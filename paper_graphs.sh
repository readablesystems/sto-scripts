#!/bin/bash

./plotter.py y_base t_base w_base r_base tpcc-index-contention \
             t_noncumu_o t_xsys t_semopt t_semind \
             y_semopt w_scale_merged r_scale_merged -tpdf -n
