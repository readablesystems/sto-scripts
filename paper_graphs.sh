#!/bin/bash

plots=(
  y_base
  t_base
  w_base
  r_base
  t_idxcont
  t_noncumu_o
  t_noncumu_t
  t_noncumu_m
  t_xsys
  t_semopt
  t_semind
  y_semopt
  w_scale_merged
  r_scale_merged
  r_semopt
  w_semopt
  t_scale_m
  t_scale_m_past
  )

for plot in ${plots[@]}; do
  ./plotter.py $plot -tpdf -n
done
