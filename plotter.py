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

from config import TOCCGraphConfig, TMVGraphConfig, WikiOCCGraphConfig, WikiMVGraphConfig
from config import RubisOCCGraphConfig, RubisMVGraphConfig
from config import TW1OCCZoomedGraphConfig, TW1MVZoomedGraphConfig
from config import TWPOCCGraphConfig, TWPMVGraphConfig
from config import TPCCFactorsGraphConfig

from config import TPCCOpacityGraphConfig
from config import TOCCCompGraphConfig, TMVCompGraphConfig

from config import color_mapping, marker_mapping
from runner import BenchRunner

# Common files and definitions needed to process experiment result files and draw graphs

plotter_map = {
    'tpcc': TPCCGraphConfig,
    'wiki': WikiGraphConfig,
    't_scale_o': TOCCGraphConfig,
    't_scale_m': TMVGraphConfig,
    'w_scale_o': WikiOCCGraphConfig,
    'w_scale_m': WikiMVGraphConfig,
    'r_scale_o': RubisOCCGraphConfig,
    'r_scale_m': RubisMVGraphConfig,
    'tw1_zoomed_o': TW1OCCZoomedGraphConfig,
    'tw1_zoomed_m': TW1MVZoomedGraphConfig,
    'twp_line_o': TWPOCCGraphConfig,
    'twp_line_m': TWPMVGraphConfig,
    'tpccfactors': TPCCFactorsGraphConfig,
    'tpccopacity': TPCCOpacityGraphConfig,
    't_comp_o': TOCCCompGraphConfig,
    't_comp_m': TMVCompGraphConfig,
    'mvsto': MVSTOGraphConfig,
    'mvsto-occ': MVSTOTPCCOCCGraphConfig,
    'mvsto-mvcc': MVSTOTPCCMVCCGraphConfig,
    'mvstoycsb': MVSTOYCSBGraphConfig,
    'mvstoycsb-occ': MVSTOYCSBOCCGraphConfig,
    'mvstoycsb-mvcc': MVSTOYCSBMVCCGraphConfig,
    'mvstowiki': MVSTOWikiGraphConfig,
    'mvstorubis': MVSTORubisGraphConfig
}


def file_timestamp_str():
    dt_now = datetime.datetime.now()
    return '{:04d}{:02d}{:02d}{:02d}'.format(dt_now.year, dt_now.month, dt_now.day, dt_now.hour)


class GraphGlobalConstants:
    FONT_SIZE = 22
    FIG_SIZE = (10, 6)
    BAR_WIDTH_SCALE_FACTOR = 1.3
    ERROR_KW = dict(ecolor='red', elinewidth=2, capsize=4, capthick=2)
    TABLEAU20 = [(31,119,180), (174,199,232), (255,127,14), (255,187,120),
                 (44,160,44), (152,223,138), (214,39,40), (255,152,150),
                 (148,103,189), (197,176,213), (140,86,75), (196,156,148),
                 (227,119,194), (247,182,210), (127,127,127), (199,199,199),
                 (188,189,34), (219,219,141), (23,190,207), (158,218,229)]

    @classmethod
    def set_tableau20(cls):
        for i in range(len(cls.TABLEAU20)):
            r,g,b = cls.TABLEAU20[i]
            cls.TABLEAU20[i] = (r/255., g/255., b/255.)


class BenchPlotter:
    show_only = True
    img_fmt = 'pdf'
    plot_aborts = False

    @classmethod
    def set_matplotlib_params(cls):
        fnt_sz = GraphGlobalConstants.FONT_SIZE

        mpl.rcParams['figure.figsize'] = GraphGlobalConstants.FIG_SIZE
        mpl.rcParams['figure.dpi'] = 80
        mpl.rcParams['savefig.dpi'] = 80

        mpl.rcParams['lines.markersize'] = 11
        mpl.rcParams['font.size'] = fnt_sz
        mpl.rcParams['axes.titlesize'] = fnt_sz
        mpl.rcParams['axes.labelsize'] = fnt_sz
        mpl.rcParams['xtick.labelsize'] = fnt_sz
        mpl.rcParams['ytick.labelsize'] = fnt_sz
        mpl.rcParams['legend.fontsize'] = 16
        mpl.rcParams['figure.titlesize'] = 'medium'

    @classmethod
    def key(cls, d1, d2, d3):
        return '{0}/{1}/{2}'.format(d3, d2, d1)

    def __init__(self, info, graph_type, dim1, dim2, dim3, legends, d3t, d3f):
        self.graph_info = info.copy()
        self.graph_type = graph_type
        self.dimension1 = dim1
        self.dimension2 = dim2
        self.dimension3 = dim3
        self.legends = legends
        self.d3titles = d3t
        self.d3fnames = d3f

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

                        #med_idx = xput_series.index(xput_med)

                        rec = [[xput_min, xput_med, xput_max],
                               abrts_med,
                               cabrts_med]

                        processed_results[BenchPlotter.key(thr, sut, cnf)] = rec

        return processed_results

    def pack_xput_data(self, processed_results, d3, legends, graph_title, save_name):
        print("xput:")
        meta = self.graph_info.copy()
        common_x = self.dimension1
        y_series = []
        y_errors = []
        for sut in self.dimension2:
            print(sut)
            series_data = []
            series_error_down = []
            series_error_up = []
            for thr in self.dimension1:
                bplt_key = BenchPlotter.key(thr, sut, d3)
                try:
                    res = processed_results[bplt_key]
                    xput = res[0]
                    series_data.append(xput[1] / 1000000.0)
                    series_error_down.append((xput[1] - xput[0]) / 1000000.0)
                    series_error_up.append((xput[2] - xput[1]) / 1000000.0)
                except KeyError:
                    print('Result key {} not found.'.format(bplt_key))
                    series_data.append(0)
                    series_error_down.append(0)
                    series_error_up.append(0)
            print(series_data)
            y_series.append(series_data)
            y_errors.append((series_error_down, series_error_up))

        meta['graph_title'] = graph_title
        meta['save_name'] = save_name
        meta['legends_on'] = legends

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
        for i,y in enumerate(y_series):
            if y != 0:
                out_x.append(common_x[i])
                out_y.append(y)
                out_y_err[0].append(y_errors[0][i])
                out_y_err[1].append(y_errors[1][i])
        return out_x, out_y, out_y_err

    def draw_bars(self, meta_info, common_x, y_series, y_errors):
        fig, ax = plt.subplots(figsize=(10, 6))

        N = len(common_x)
        width = 0.1
        ind = np.arange(N) + 2 * width

        num_series = len(self.dimension2)

        rects = []

        for i in range(num_series):
            f_color = GraphGlobalConstants.TABLEAU20[color_mapping[self.dimension2[i]]]
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
            ax.legend([r[0] for r in rects],
                      [meta_info['series_names'][i] for i in range(num_series)],
                      loc='best')

        plt.tight_layout()
        if BenchPlotter.show_only:
            plt.show()
        else:
            plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))

    def draw_lines(self, meta_info, common_x, y_series, y_errors):
        fig, ax = plt.subplots(figsize=(10, 6))
        num_series = len(self.dimension2)
        lines = []
        for i in range(num_series):
            l_color = GraphGlobalConstants.TABLEAU20[color_mapping[self.dimension2[i]]]
            l_marker = marker_mapping[self.dimension2[i]]
            p_x, p_y, p_err = self.strip_zeros_in_xyseries(common_x, y_series[i], y_errors[i])
            l = ax.errorbar(p_x, p_y, marker=l_marker, color=l_color, yerr=p_err, ecolor=l_color, capsize=4)
            lines.append(l)

        if meta_info['graph_title'] != '':
            ax.set_title(meta_info['graph_title'])
        ax.set_ylabel(meta_info['y_label'])
        ax.set_ylim(bottom=0)
        if 'y_max' in meta_info:
            ax.set_ylim(top=meta_info['y_max'])
        ax.set_xlabel(meta_info['x_label'])

        if meta_info['legends_on']:
            ax.legend([l[0] for l in lines],
                      [meta_info['series_names'][i] for i in range(num_series)],
                      loc='best')
        plt.tight_layout()
        if BenchPlotter.show_only:
            plt.show()
        else:
            plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))

    def draw_hbars(self, meta_info, common_x, y_series, y_errors):
        # common_x is ignored
        fig, ax = plt.subplots(figsize=(10, 6))
        num_series = len(self.dimension2)
        y_pos = np.arange(num_series)

        y_flat_data = []
        y_flat_err = []
        # flatten inner lists
        for idx in range(num_series):
            y_flat_data.append(y_series[idx][0])
            y_flat_err.append(y_errors[idx][0])

        ax.barh(y_pos, y_flat_data, xerr=y_flat_err, align='center', color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(meta_info['series_names'])
        ax.set_xlim(left=0)
        ax.set_xlabel(meta_info['y_label'])

        plt.tight_layout()
        if BenchPlotter.show_only:
            plt.show()
        else:
            plt.savefig('{}_{}.{}'.format(meta_info['save_name'], file_timestamp_str(), BenchPlotter.img_fmt))

    def draw_all(self, results):
        processed = self.process(results)

        print('--throughput graph(s)--')
        for idx in range(len(self.dimension3)):
            d3 = self.dimension3[idx]
            legends = self.legends[idx]
            title = self.d3titles[idx]
            fname = self.d3fnames[idx]
            if self.graph_type == GraphType.BAR:
                self.draw_bars(*self.pack_xput_data(processed, d3, legends, title, fname))
            elif self.graph_type == GraphType.LINE:
                self.draw_lines(*self.pack_xput_data(processed, d3, legends, title, fname))
            elif self.graph_type == GraphType.HBAR:
                self.draw_hbars(*self.pack_xput_data(processed, d3, legends, title, fname))

        if self.plot_aborts:
            print('--abort graph(s)--')
            for idx in range(len(self.dimension3)):
                d3 = self.dimension3[idx]
                title = self.d3titles[idx] + ' (abort rates)'
                fname = self.d3fnames[idx] + '_aborts'
                self.draw_lines(*self.pack_abrts_data(processed, d3, title, fname))


def get_plotter(bench_name):
    cnf = plotter_map[bench_name]
    return BenchPlotter(cnf.INFO, cnf.TYPE, cnf.DIM1, cnf.DIM2, cnf.DIM3, cnf.LEGENDS, cnf.D3TITLES, cnf.D3FNAMES), \
           config.get_result_file(cnf.NAME)


if __name__ == '__main__':
    GraphGlobalConstants.set_tableau20()
    BenchPlotter.set_matplotlib_params()
    usage = "Usage: %prog benchmark\n\nSupported benchmarks: "
    usage += ', '.join(plotter_map.keys())
    psr = optparse.OptionParser(usage=usage)
    psr.add_option("-a", "--plot-aborts", action="store_true", dest="plot_aborts", default=False,
                   help="Set if want to plot abort graphs (in addition to throughput graphs).")
    psr.add_option("-f", "--save-to-file", action="store_true", dest="save_file", default=False,
                   help="Set if want to save graph as file. (Default False, show figure only).")
    psr.add_option("-t", "--image-type", action="store", type="string", dest="ext", default="",
                   help="Set the image type (pdf/png). Implies --save-to-file.")

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

    if len(args) == 0:
        psr.error("Please specificy at least one benchmark to plot.");

    for arg in args:
        if not arg in plotter_map:
            psr.error("Unknown benchmark: {}.".format(arg))

        plotter, result_file = get_plotter(arg)
        results = {}
        try:
            with open(result_file, 'r') as rf:
                results = json.load(rf)
        except:
            config.fatal_error('Can not open result file: {}. Did you run the benchmark first?'.format(result_file))
        plotter.draw_all(results)
