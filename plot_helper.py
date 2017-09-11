#!/usr/bin/env python

BAR_WIDTH_SACLE_FACTOR = 1.3

def second_xtick_labels(fig, orig_ax, first_tick_locations, labels):
    lim = orig_ax.get_xlim()
    ax2 = orig_ax.twiny()

    N = len(first_tick_locations)

    fig.subplots_adjust(bottom=0.2)
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")

    ax2.spines["bottom"].set_position(("axes", -0.1))

    second_tick_locations = [(first_tick_locations[0]+first_tick_locations[(N-1)/2-1])/2,
        (first_tick_locations[(N-1)/2+1]+first_tick_locations[N-1])/2]
        
    ax2.set_frame_on(True)
    ax2.patch.set_visible(False)
    for sp in ax2.spines.itervalues():
        sp.set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.tick_params(axis=u'both', which=u'both',length=0)

    ax2.set_xticks(second_tick_locations)
    ax2.set_xticklabels(labels)
    ax2.set_xlim(lim)
