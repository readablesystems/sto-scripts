#!/usr/bin/env python3
import json
import optparse
import datetime

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt

import config
from config import fatal_error
from config import GraphType
from config import WikiGraphConfig, TPCCGraphConfig, MVSTOGraphConfig, MVSTOWikiGraphConfig
from config import MVSTOTPCCOCCGraphConfig, MVSTOTPCCMVCCGraphConfig, MVSTOYCSBGraphConfig
from config import MVSTOYCSBOCCGraphConfig, MVSTOYCSBMVCCGraphConfig, MVSTORubisGraphConfig

from config import YOCCGraphConfig, YMVGraphConfig, YTOCompGraphConfig
from config import YScalabilityMergedGraphConfig, YCSBBaselinesGraphConfig
from config import YCSBSemanticOptGraphConfig, YCSBSemanticIndGraphConfig
from config import YCSBCollapseGraphConfig, YCSBCollapseBaselinesGraphConfig
from config import TOCCGraphConfig, TMVGraphConfig, TMVPastGraphConfig
from config import WikiOCCGraphConfig, WikiMVGraphConfig
from config import RubisOCCGraphConfig, RubisMVGraphConfig
from config import WikiSemanticOptGraphConfig, RubisSemanticOptGraphConfig
from config import WikiBaselineGraphConfig, RubisBaselineGraphConfig
from config import TW1OCCZoomedGraphConfig, TW1MVZoomedGraphConfig
from config import TWPOCCGraphConfig, TWPMVGraphConfig
from config import TPCCFactorsGraphConfig, TPCCStackedFactorsGraphConfig, TPCCOCCStackedFactorsGraphConfig
from config import TPCCNonCumuFactorsMVCCGraphConfig, TPCCNonCumuFactorsOCCGraphConfig, TPCCNonCumuFactorsTTCCGraphConfig, OldTPCCNonCumuFactorsOCCGraphConfig
from config import TPCCIndexContentionGraphConfig

from config import TScalabilityMergedGraphConfig
from config import TPCCBaselinesGraphConfig, TPCCXSystemGraphConfig
from config import TPCCSemanticOptGraphConfig, TPCCSemanticIndGraphConfig
from config import TPCCTicTocPhantomProtectionGraphConfig, TPCCMVCCTsImplGraphConfig, TPCCMVCCCuImplGraphConfig
from config import TPCCHistoryKeyBaselineGraphConfig, TPCCHistoryKeySemoptGraphConfig
from config import TPCCDramaticGraphConfig

from config import TPCCOpacityGraphConfig
from config import TOTCCCompGraphConfig
from config import TOCCCompGraphConfig, TMVCompGraphConfig
from config import TMVFlattenGraphConfig, TMVGCIntervalGraphConfig

from config import color_mapping, marker_mapping, linestyle_mapping, linewidth_mapping, errorbar_mapping, \
    barcolor_mapping
from runner import BenchRunner

# Common files and definitions needed to process experiment result files and draw graphs

plotter_map = {
    'tpcc': TPCCGraphConfig,
    'wiki': WikiGraphConfig,
    'y_scale_o': YOCCGraphConfig,
    'y_scale_m': YMVGraphConfig,
    'y_tictoc_comp': YTOCompGraphConfig,
    'y_base': YCSBBaselinesGraphConfig,
    'y_semopt': YCSBSemanticOptGraphConfig,
    'y_semind': YCSBSemanticIndGraphConfig,
    'y_collapse': YCSBCollapseGraphConfig,
    'y_collapse_base': YCSBCollapseBaselinesGraphConfig,
    'y_scale_merged': YScalabilityMergedGraphConfig,
    't_scale_o': TOCCGraphConfig,
    't_scale_m': TMVGraphConfig,
    't_scale_m_past': TMVPastGraphConfig,
    't_scale_merged': TScalabilityMergedGraphConfig,
    't_base': TPCCBaselinesGraphConfig,
    't_xsys': TPCCXSystemGraphConfig,
    't_semopt': TPCCSemanticOptGraphConfig,
    't_semind': TPCCSemanticIndGraphConfig,
    't_ttcc_pp': TPCCTicTocPhantomProtectionGraphConfig,
    't_mvp': TPCCMVCCTsImplGraphConfig,
    't_mcp': TPCCMVCCCuImplGraphConfig,
    't_hkbase': TPCCHistoryKeyBaselineGraphConfig,
    't_hksemopt': TPCCHistoryKeySemoptGraphConfig,
    't_dramatic': TPCCDramaticGraphConfig,
    'w_scale_o': WikiOCCGraphConfig,
    'w_scale_m': WikiMVGraphConfig,
    'w_base': WikiBaselineGraphConfig,
    'w_semopt': WikiSemanticOptGraphConfig,
    'r_scale_o': RubisOCCGraphConfig,
    'r_scale_m': RubisMVGraphConfig,
    'r_base': RubisBaselineGraphConfig,
    'r_semopt': RubisSemanticOptGraphConfig,
    'tw1_zoomed_o': TW1OCCZoomedGraphConfig,
    'tw1_zoomed_m': TW1MVZoomedGraphConfig,
    'twp_line_o': TWPOCCGraphConfig,
    'twp_line_m': TWPMVGraphConfig,
    'tpccfactors': TPCCFactorsGraphConfig,
    't_noncumu_m': TPCCNonCumuFactorsMVCCGraphConfig,
    't_noncumu_o': TPCCNonCumuFactorsOCCGraphConfig,
    't_noncumu_t': TPCCNonCumuFactorsTTCCGraphConfig,
    'old_t_noncumu_o': OldTPCCNonCumuFactorsOCCGraphConfig,
    'tpcc-stacked-factors': TPCCStackedFactorsGraphConfig,
    'tpcc-stacked-factors-occ': TPCCOCCStackedFactorsGraphConfig,
    't_idxcont': TPCCIndexContentionGraphConfig,
    'tpccopacity': TPCCOpacityGraphConfig,
    't_comp_t': TOTCCCompGraphConfig,
    't_comp_o': TOCCCompGraphConfig,
    't_comp_m': TMVCompGraphConfig,
    't_flatten': TMVFlattenGraphConfig,
    't_gc': TMVGCIntervalGraphConfig,
    'mvsto': MVSTOGraphConfig,
    'mvsto-occ': MVSTOTPCCOCCGraphConfig,
    'mvsto-mvcc': MVSTOTPCCMVCCGraphConfig,
    'mvstoycsb': MVSTOYCSBGraphConfig,
    'mvstoycsb-occ': MVSTOYCSBOCCGraphConfig,
    'mvstoycsb-mvcc': MVSTOYCSBMVCCGraphConfig,
    'mvstowiki': MVSTOWikiGraphConfig,
    'mvstorubis': MVSTORubisGraphConfig
}

# Configure default figure sizes for thesis or VLDB paper.
FIG_SIZE_FOR = 'thesis' # use 'vldb' for smaller sizes


def prop_mapping(m, sut):
    if not sut:
        return None
    if sut in m:
        return m[sut]
    if sut.endswith('-secondary') and 'secondary' in m:
        return m['secondary']
    if 'default' in m:
        return m['default']
    return None


class GraphGlobalConstants:
    FONT_SIZE = 22
    FIG_SIZE = (8.333, 5) if FIG_SIZE_FOR == 'thesis' else (5, 5)
    WIDE_FIG_SIZE = (12, 5)
    BAR_WIDTH_SCALE_FACTOR = 1.3
    ERROR_KW = dict(ecolor='black', elinewidth=1.5, capsize=6, capthick=1.5)
    TABLEAU20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    @classmethod
    def color(cls, color):
        if isinstance(color, int):
            color = cls.TABLEAU20[color]
        elif isinstance(color, str):
            return color
        if not color:
            return 'none'
        elif color[0] > 1 or color[1] > 1 or color[2] > 1:
            return (color[0] / 255., color[1] / 255., color[2] / 255.)
        else:
            return color


class BenchPlotter:
    show_only = True
    img_fmt = 'pdf'
    plot_aborts = False
    write_timestamp = True

    def set_matplotlib_params(self):
        fnt_sz = GraphGlobalConstants.FONT_SIZE

        mpl.rcParams['figure.figsize'] = self.figsize
        mpl.rcParams['figure.dpi'] = 80
        mpl.rcParams['savefig.dpi'] = 80

        mpl.rcParams['lines.markeredgewidth'] = 1.5
        mpl.rcParams['lines.markersize'] = 9
        mpl.rcParams['font.size'] = fnt_sz
        mpl.rcParams['font.family'] = 'Arial'
        mpl.rcParams['axes.titlesize'] = fnt_sz
        mpl.rcParams['axes.labelsize'] = fnt_sz
        mpl.rcParams['xtick.labelsize'] = fnt_sz
        mpl.rcParams['ytick.labelsize'] = fnt_sz
        mpl.rcParams['legend.fontsize'] = self.legend_fnt_sz
        mpl.rcParams['figure.titlesize'] = 'medium'

    @classmethod
    def file_timestamp_str(cls):
        if cls.write_timestamp:
            dt_now = datetime.datetime.now()
            return '{:04d}{:02d}{:02d}{:02d}'.format(dt_now.year, dt_now.month, dt_now.day, dt_now.hour)
        else:
            return 'latest'

    @classmethod
    def key(cls, d1, d2, d3):
        if d2 and d2.endswith('-secondary'):
            d2 = d2[0:len(d2) - 10]
        return '{0}/{1}/{2}'.format(d3, d2, d1)

    def __init__(self, cnf):
        self.graph_info = cnf.INFO.copy()
        self.graph_type = cnf.TYPE
        self.dimension1 = cnf.DIM1
        self.dimension2 = cnf.DIM2
        if hasattr(cnf, "SUBFIG_DIM2S"):
            self.subfigure_dimension2 = cnf.SUBFIG_DIM2S
            if self.dimension2 is None:
                self.dimension2 = [sut for subfig in self.subfigure_dimension2 for sut in subfig]
        else:
            self.subfigure_dimension2 = None
        if hasattr(cnf, "LEGEND_FONT_SIZE"):
            self.legend_fnt_sz = cnf.LEGEND_FONT_SIZE
        else:
            self.legend_fnt_sz = 16
        self.dimension3 = cnf.DIM3
        self.legends = cnf.LEGENDS
        if hasattr(cnf, "LEGEND_SELECT"):
            self.legend_select = cnf.LEGEND_SELECT
        else:
            self.legend_select = [(0, len(self.dimension2)) for i in range(len(self.dimension3))]
        self.d3ymaxes = cnf.D3YMAXES
        self.d3titles = cnf.D3TITLES
        self.d3fnames = cnf.D3FNAMES
        self.datanames = [cnf.NAME]
        if hasattr(cnf, "DATANAMES"):
            for n in cnf.DATANAMES:
                self.datanames.push(n)
        self.figsize = GraphGlobalConstants.FIG_SIZE
        self.wide_figsize = GraphGlobalConstants.WIDE_FIG_SIZE
        if hasattr(cnf, "FIG_SIZE"):
            self.figsize = cnf.FIG_SIZE
        if hasattr(cnf, "WIDE_FIG_SIZE"):
            self.wide_figsize = cnf.WIDE_FIG_SIZE
        print(self.figsize)

    def process(self, results):
        processed_results = {}
        messaged = False
        for cnf in self.dimension3:
            for sut in self.dimension2:
                for thr in self.dimension1:
                    xput_series = []
                    abrts_series = []
                    cabrts_series = []
                    for n in range(100):
                        k = BenchRunner.key(thr, sut, cnf, n)
                        try:
                            (xput, abrts, cabrts) = results[k]
                            xput_series.append(xput)
                            abrts_series.append(abrts)
                            cabrts_series.append(cabrts)
                        except KeyError:
                            break

                    if (not messaged) and (len(xput_series) != BenchRunner.num_trails):
                        print('INFO: Processed experiment with {} trails.'.format(len(xput_series)))
                        messaged = True

                    if len(xput_series) > 0:
                        xput_med = np.median(xput_series)
                        xput_min = np.amin(xput_series)
                        xput_max = np.amax(xput_series)

                        abrts_med = np.median(abrts_series)
                        cabrts_med = np.median(cabrts_series)

                        # med_idx = xput_series.index(xput_med)

                        rec = [[xput_min, xput_med, xput_max],
                               abrts_med,
                               cabrts_med]

                        processed_results[BenchPlotter.key(thr, sut, cnf)] = rec

        return processed_results

    def pack_xput_data(self, processed_results, dim2, d3, legends, graph_y_max, graph_title):
        print("xput:")
        meta = self.graph_info.copy()
        # Default scale factor is 1 million
        scale_factor = 1000000.0
        if 'scale_factor' in meta.keys():
            scale_factor = meta['scale_factor']
        common_x = self.dimension1
        y_series = []
        y_errors = []

        # dimension2 is systems under comparison. Can either be supplied or use the default configuration.
        dimension2 = self.dimension2 if dim2 is None else dim2
        for sut in dimension2:
            print(sut)
            series_data = []
            series_error_down = []
            series_error_up = []
            for thr in self.dimension1:
                bplt_key = BenchPlotter.key(thr, sut, d3)
                try:
                    res = processed_results[bplt_key]
                    xput = res[0]
                    series_data.append(xput[1] / scale_factor)
                    series_error_down.append((xput[1] - xput[0]) / scale_factor)
                    series_error_up.append((xput[2] - xput[1]) / scale_factor)
                except KeyError:
                    print('Result key {} not found.'.format(bplt_key))
                    series_data.append(0)
                    series_error_down.append(0)
                    series_error_up.append(0)
            print(series_data)
            y_series.append(series_data)
            y_errors.append((series_error_down, series_error_up))

        meta['graph_title'] = graph_title
        meta['legends_on'] = legends
        meta['d3'] = d3

        if graph_y_max is not None:
            meta['y_max'] = graph_y_max

        return meta, common_x, y_series, y_errors

    def pack_abrts_data(self, processed_results, d3, graph_title, save_name):
        print("aborts:")
        meta = self.graph_info.copy()
        common_x = self.dimension1
        y_series = []
        y_errors = []
        for sut in self.dimension2:
            print(sut)
            series_data = []
            for thr in self.dimension1:
                res = processed_results[BenchPlotter.key(thr, sut, d3)]
                series_data.append(res[1])

            print(series_data)
            y_series.append(series_data)
            y_errors.append(None)

        meta['y_label'] = 'Abort Rate (%)'
        meta['graph_title'] = graph_title
        meta['save_name'] = save_name

        return meta, common_x, y_series, y_errors

    # Assuming that y_errors is an (2, N)-dimension array
    # First row contains upper errors, second row contains low errors
    def strip_zeros_in_xyseries(self, common_x, y_series, y_errors):
        if (len(y_errors) != 2) or (len(y_errors[0]) != len(y_errors[1])):
            fatal_error('y_errors dimension invalid.')
        if (len(common_x) != len(y_series)) or (len(common_x) != len(y_errors[0])):
            fatal_error('x-y series dimension mismatch.')
        out_x = []
        out_y = []
        out_y_err = [[], []]
        for i, y in enumerate(y_series):
            if y != 0:
                out_x.append(common_x[i])
                out_y.append(y)
                out_y_err[0].append(y_errors[0][i])
                out_y_err[1].append(y_errors[1][i])
        return out_x, out_y, out_y_err

    def series_names(self, meta_info):
        series_names = meta_info['series_names']
        result = []
        for i, sut in enumerate(self.dimension2):
            if isinstance(series_names, tuple):
                if i < len(series_names):
                    result.append(series_names[i])
                else:
                    break
            else:
                if sut in series_names:
                    result.append(series_names[sut])
                else:
                    break
        return result

    def draw_bars(self, meta_info, common_x, y_series, y_errors):
        fig, ax = plt.subplots(figsize=self.figsize)

        N = len(common_x)
        width = 0.1
        ind = np.arange(N) + 2 * width

        num_series = len(self.dimension2)

        rects = []

        for i in range(num_series):
            f_color = GraphGlobalConstants.color(prop_mapping(color_mapping, self.dimension2[i]))
            r = ax.bar(ind + width * i, y_series[i], width,
                       color=f_color,
                       yerr=y_errors[i], error_kw=GraphGlobalConstants.ERROR_KW)
            rects.append(r)

        if meta_info['graph_title'] != '':
            ax.set_title(meta_info['graph_title'])
        ax.set_ylabel(meta_info['y_label'])
        ax.set_ylim(bottom=0)
        ax.set_xticks(ind + width * num_series / 2)
        ax.set_xticklabels(['{}'.format(t) for t in common_x])
        ax.set_xlabel(meta_info['x_label'])

        if meta_info['legends_on']:
            if 'legend_ncol' in meta_info.keys():
                legend_n_columns = meta_info['legend_ncol']
            else:
                legend_n_columns = 1
            ax.legend([r[0] for r in rects], self.series_names(meta_info),
                      loc='best', ncol=legend_n_columns)

        plt.tight_layout()
        if BenchPlotter.show_only:
            plt.show()
        else:
            plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))
        plt.close(fig)

    def draw_lines(self, ax, subfig_idx, legend_select, series_names, dim2, meta_info, common_x, y_series, y_errors):
        #fig, ax = plt.subplots(figsize=self.figsize)
        ls0 = legend_select[0]
        ls1 = legend_select[1]
        num_series = len(y_series)
        use_dimension2 = self.dimension2 if dim2 is None else dim2
        lines = []
        markevery_map = meta_info.get('markevery')
        for i in range(num_series):
            sut = use_dimension2[i]
            l_color = GraphGlobalConstants.color(prop_mapping(color_mapping, sut))
            l_marker = prop_mapping(marker_mapping, sut)
            if meta_info.get('markers') is False:
                l_marker = None
            l_width = prop_mapping(linewidth_mapping, sut)
            l_style = prop_mapping(linestyle_mapping, sut)
            p_x, p_y, p_err = self.strip_zeros_in_xyseries(common_x, y_series[i], y_errors[i])

            markevery = None
            if markevery_map is not None:
                sutd3 = '{}/{}'.format(sut, meta_info['d3'])
                print('sutd3:', sutd3)
                if sutd3 in markevery_map:
                    markevery = markevery_map[sutd3]
                elif sut in markevery_map:
                    markevery = markevery_map[sut]
                elif sut and sut.endswith('-secondary') and 'secondary' in markevery_map:
                    markevery = markevery_map['secondary']
                else:
                    markevery = markevery_map.get('default')

            args = {
                'marker': l_marker,
                'color': l_color,
                'linewidth': l_width,
                'linestyle': l_style,
                'markevery': markevery,
                }
            if prop_mapping(errorbar_mapping, sut):
                l = ax.errorbar(p_x, p_y, yerr=p_err, ecolor=l_color, capsize=4, **args)
            else:
                l = ax.plot(p_x, p_y, **args)
            lines.append(l)

        if meta_info['graph_title'] != '':
            ax.set_title(meta_info['graph_title'])
        if subfig_idx == 0:
            ax.set_ylabel(meta_info['y_label'])
            ax.set_ylim(bottom=0)
            if 'y_max' in meta_info:
                ax.set_ylim(top=meta_info['y_max'])
        ax.set_xlabel(meta_info['x_label'])
        ax.tick_params('y', left=True, right=True)

        if meta_info['legends_on']:
            slines = [l[0] for l in lines]
            snames = self.series_names(meta_info) if series_names is None else series_names

            if 'legend_ncol' in meta_info.keys():
                legend_n_columns = meta_info['legend_ncol']
            else:
                legend_n_columns = 1
            if meta_info.get('legend_order') is not None:
                xlines = []
                xnames = []
                for i in meta_info['legend_order']:
                    xlines.append(slines[i])
                    xnames.append(snames[i])
                ax.legend(xlines[ls0:ls1], xnames[ls0:ls1], loc='best', framealpha=0, ncol=legend_n_columns)
            else:
                ax.legend(slines[ls0:ls1], snames[ls0:ls1], loc='best', framealpha=0, ncol=legend_n_columns)

        #plt.tight_layout()
        #if BenchPlotter.show_only:
        #    plt.show()
        #else:
        #    plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))

    def draw_hbars(self, meta_info, common_x, y_series, y_errors):
        # common_x is ignored
        fig, ax = plt.subplots(figsize=self.figsize)
        num_series = len(self.dimension2)
        y_pos = np.arange(num_series)

        y_flat_data = []
        y_flat_err = []
        y_color = []
        # flatten inner lists
        for idx in range(num_series):
            y_flat_data.append(y_series[idx][0])
            y_flat_err.append(y_errors[idx][0])
            y_color.append(GraphGlobalConstants.color(prop_mapping(barcolor_mapping, self.dimension2[idx])))

        ax.barh(y_pos, y_flat_data, xerr=y_flat_err, align='center', color=y_color, ecolor='black',
                error_kw=GraphGlobalConstants.ERROR_KW)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(meta_info['series_names'])
        ax.set_xlim(left=0)
        ax.set_xlabel(meta_info['y_label'])

        plt.tight_layout()
        if BenchPlotter.show_only:
            plt.show()
        else:
            plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))

    # draw_all() draws all subfigures specified in a certain graph config. It either draws individual subfigures or
    # draws a single combined figure with shared x or y axis based on graph configuration.
    def draw_all(self, results):
        self.set_matplotlib_params()
        processed = self.process(results)

        if 'combine_subfigures' in self.graph_info.keys():
            print('--combine subfigures--')
            combine_mode = self.graph_info['combine_subfigures']
            share_y = combine_mode == 'share-y'
            if not share_y:
                assert combine_mode == 'share-x', 'Unrecognized subfigure combine mode: {}.'.format(combine_mode)


            for idx, d3 in enumerate(self.dimension3):
                legends = self.legends[idx]
                ymax = self.d3ymaxes[idx]
                title = self.d3titles[idx]
                fname = self.d3fnames[idx]
                legend_select = self.legend_select[idx]

                num_subfigures = len(self.subfigure_dimension2)
                if share_y:
                    fig, ax = plt.subplots(1, num_subfigures, sharey=True, figsize=self.wide_figsize,
                                           gridspec_kw={'wspace':0.0})
                else:
                    fig, ax = plt.subplots(num_subfigures, 1, sharex=True, figsize=self.wide_figsize,
                                           gridspec_kw={'hspace':0.0})

                for didx, d2 in enumerate(self.subfigure_dimension2):
                    d2_series_names = self.graph_info['subfigure_series_names'][didx]
                    if self.graph_type == GraphType.BAR:
                        self.draw_bars(ax[didx], *self.pack_xput_data(processed, d2, d3, legends, ymax, title))
                    elif self.graph_type == GraphType.LINE:
                        self.draw_lines(ax[didx], didx, legend_select, d2_series_names, d2, *self.pack_xput_data(processed, d2, d3, legends, ymax, title))
                    else:
                        assert False, 'Only bar graph and line graph are supported when combining subfigures.'

                plt.tight_layout()
                if BenchPlotter.show_only:
                    plt.show()
                else:
                    plt.savefig('{}_{}.{}'.format(fname, self.file_timestamp_str(), BenchPlotter.img_fmt))
                plt.close(fig)
        else:
            print('--throughput graph(s)--')
            for idx, d3 in enumerate(self.dimension3):
                legends = self.legends[idx]
                ymax = self.d3ymaxes[idx]
                title = self.d3titles[idx]
                fname = self.d3fnames[idx]
                legend_select = self.legend_select[idx]

                fig, ax = plt.subplots(figsize=self.figsize)
                if self.graph_type == GraphType.BAR:
                    self.draw_bars(ax, *self.pack_xput_data(processed, None, d3, legends, ymax, title))
                elif self.graph_type == GraphType.LINE:
                    self.draw_lines(ax, 0, legend_select, None, None, *self.pack_xput_data(processed, None, d3, legends, ymax, title))
                elif self.graph_type == GraphType.HBAR:
                    self.draw_hbars(ax, *self.pack_xput_data(processed, None, d3, legends, ymax, title))

                plt.tight_layout()
                if BenchPlotter.show_only:
                    plt.show()
                else:
                    plt.savefig('{}_{}.{}'.format(fname, self.file_timestamp_str(), BenchPlotter.img_fmt))
                plt.close(fig)

        if self.plot_aborts:
            print('--abort graph(s)--')
            for idx in range(len(self.dimension3)):
                d3 = self.dimension3[idx]
                title = self.d3titles[idx] + ' (abort rates)'
                fname = self.d3fnames[idx] + '_aborts'
                self.draw_lines(*self.pack_abrts_data(processed, d3, title, fname))


def get_plotter(bench_name):
    return BenchPlotter(plotter_map[bench_name])


def merge_results(results, name):
    file = config.get_result_file(name)
    try:
        print(file)
        with open(file, 'r') as rf:
            results.update(json.load(rf))
    except:
        config.fatal_error('Can not open result file: {}. Did you run the benchmark first?'.format(file))


if __name__ == '__main__':
    usage = "Usage: %prog benchmark\n\nSupported benchmarks: "
    usage += ', '.join(plotter_map.keys())
    psr = optparse.OptionParser(usage=usage)
    psr.add_option("-a", "--plot-aborts", action="store_true", dest="plot_aborts", default=False,
                   help="Set if want to plot abort graphs (in addition to throughput graphs).")
    psr.add_option("-f", "--save-to-file", action="store_true", dest="save_file", default=False,
                   help="Set if want to save graph as file. (Default False, show figure only).")
    psr.add_option("-t", "--image-type", action="store", type="string", dest="ext", default="",
                   help="Set the image type (pdf/png). Implies --save-to-file.")
    psr.add_option("-n", "--no-timestamp", action="store_false", dest="write_timestamp", default=True,
                   help="Write \"latest\" instead of the timestamp to end of the file name.")

    supported_exts = ["pdf", "png"]

    opts, args = psr.parse_args()

    if opts.save_file:
        BenchPlotter.show_only = False
    if opts.plot_aborts:
        BenchPlotter.plot_aborts = True
    if opts.ext != "":
        if opts.ext in supported_exts:
            BenchPlotter.img_fmt = opts.ext
            BenchPlotter.show_only = False
        else:
            psr.error("Unsupported image file extension: {}.".format(opts.ext))
    if not opts.write_timestamp:
        BenchPlotter.write_timestamp = False

    if len(args) == 0:
        psr.error("Please specify at least one benchmark to plot.");

    for arg in args:
        if not arg in plotter_map:
            psr.error("Unknown benchmark: {}.".format(arg))

        plotter = get_plotter(arg)
        results = {}
        for n in plotter.datanames:
            merge_results(results, n)
        plotter.draw_all(results)
