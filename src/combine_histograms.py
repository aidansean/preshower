import math, numpy, os, string
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetFillStyle(ROOT.kWhite)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetErrorX(0)

canvas = ROOT.TCanvas('canvas','',100,100,600,600)
canvas.SetGridx()
canvas.SetGridy()

weight_names = ['raw','E','phi','EPhi']

weight_titles = {}
weight_titles['raw' ] = 'Raw'
weight_titles['E'   ] = 'Flat in E'
weight_titles['phi' ] = 'Flat in #phi'
weight_titles['EPhi'] = 'Flat in E, #phi'

weight_colors = {}
weight_colors['raw' ] = ROOT.kBlack
weight_colors['E'   ] = ROOT.kRed
weight_colors['phi' ] = ROOT.kBlue
weight_colors['EPhi'] = ROOT.kGreen

weight_markers = {}
weight_markers['raw' ] = 20
weight_markers['E'   ] = 21
weight_markers['phi' ] = 22
weight_markers['EPhi'] = 23

def style_histogram(h, type):
    h.GetXaxis().SetLabelSize(0.025)
    h.GetXaxis().SetTitleOffset(1.25)
    h.GetYaxis().SetLabelSize(0.025)
    h.GetYaxis().SetTitleOffset(1.25)

    color = ROOT.kBlack
    marker = 20
    if type == 'QCD':
        color = ROOT.kRed
        #marker = 23
        #h.SetFillStyle(3354)
    elif type=='DYEE':
        color = ROOT.kBlue
        marker = 22
        h.SetFillStyle(3345)
    elif type=='ttbar':
        color = ROOT.kGreen+2
        marker = 21
    elif type=='WW':
        color = ROOT.kMagenta+2
        marker = 22
        h.SetFillStyle(3395)
    
    h.SetMarkerStyle(marker)
    h.SetMarkerColor(color)
    h.SetLineColor(color)
    h.SetFillColor(color)

sample_names = ['ZprimeToEE_M1000','QCD']

# Make legend, labels
def make_legend(x1, y1, x2, y2):
    legend = ROOT.TLegend(x1,y1,x2,y2)
    legend.SetShadowColor(ROOT.kWhite)
    legend.SetFillColor(ROOT.kWhite)
    legend.SetBorderSize(0)
    return legend

CMS_label_texts = {}
CMS_label_texts['normal'        ] = 'CMS'
CMS_label_texts['internal'      ] = 'CMS internal'
CMS_label_texts['workInProgress'] = 'CMS work in progress'
CMS_labels = {}
for t in CMS_label_texts:
    CMS_labels[t] = ROOT.TLatex(0.65, 0.945, CMS_label_texts[t])
    CMS_labels[t].SetNDC()
CMS_label = CMS_labels['internal']


vars = []
vars.append('phi'         )
vars.append('eta'         )
vars.append('phi_cut'     )
vars.append('phi_cut_etap')
vars.append('phi_cut_etam')
vars.append('E'           )
vars.append('E_w'         )
vars.append('E_cut'       )
vars.append('ET'          )
vars.append('PSE'         )
vars.append('PSEOverEt'   )
vars.append('PSEOverE'    )
vars.append('PSEOverEz'   )
vars.append('sixix'       )
vars.append('siyiy'       )
vars.append('sirir'       )
vars.append('sixixOSiyiy' )
vars.append('sixixOSirir' )
vars.append('siyiyOSirir' )
vars.append('sixixMSiyiy' )
vars.append('ps_ix0'      )
vars.append('ps_iy0'      )
vars.append('ps_ix'       )
vars.append('ps_iy'       )
vars.append('ps_ir'       )
vars.append('ps_ixy'      )
vars.append('rxy'         )
vars.append('r9'          )
vars.append('e1x5'        )
vars.append('e2x5'        )
vars.append('fBrem'       )
vars.append('w'           )
vars.append('DR_mc'       )

f = ROOT.TFile('histograms.root','READ')

rebin_scale_0 = 4
for vname in vars:
    for wname in weight_names:
        h_ZprimeM1000 = f.Get('h_%s_ZprimeToEE_M1000_v5_%s'%(vname,wname)).Clone('h_ZprimeM1000')
        h_QCD         = f.Get('h_%s_QCD_v5_%s'             %(vname,wname)).Clone('h_QCD'        )
    
        if h_ZprimeM1000.GetSumOfWeights() < 1e-3:
            continue
        if vname=='ps_ix':
            h_ZprimeM1000.GetXaxis().SetTitle('ix^{90}(e)')
        if vname=='ps_iy':
            h_ZprimeM1000.GetXaxis().SetTitle('iy^{90}(e)')
        if vname=='ps_ixy':
            h_ZprimeM1000.GetXaxis().SetTitle('ixy^{90}(e)')
        if vname=='ps_ir':
            h_ZprimeM1000.GetXaxis().SetTitle('ir^{90}(e)')
    
        rebin_scale = 1 if ('ps_i' in vname or 'w_' in vname) else rebin_scale_0
        rebin_scale = 1
        h_QCD = h_QCD.Rebin(rebin_scale)
    
        style_histogram(h_ZprimeM1000, 'Zprime')
        style_histogram(h_QCD        , 'QCD'   )
    
        h_ZprimeM1000.Scale(1.0/h_ZprimeM1000      .GetSumOfWeights() )
        h_QCD        .Scale(1.0/(rebin_scale*h_QCD .GetSumOfWeights()))
    
        max = 0
        for h in [h_ZprimeM1000 , h_QCD]:
            val = 1.25*h.GetMaximum()
            if val > max:
                max = val
        h_ZprimeM1000.SetMinimum(0)
        h_ZprimeM1000.SetMaximum(max)
    
        legend = make_legend(0.12, 0.85, 0.88, 0.8)
        legend.SetNColumns(2)
    
        legend.AddEntry(h_ZprimeM1000, 'Z\'(1TeV)'            , 'pl')
        legend.AddEntry(h_QCD        , 'QCD'                  , 'fl')
        
        log = True if vname=='DR_mc' else False
        canvas.SetLogy(log)
        if log:
            h_ZprimeM1000.SetMinimum(1e-6)
            h_ZprimeM1000.SetMaximum(10*h_ZprimeM1000.GetMaximum())
        h_ZprimeM1000.Draw('pe')
        h_QCD.Draw('e3:sames')
        #h_QCD.Draw('pe:sames')
        h_ZprimeM1000.Draw('pe:sames')
        legend.Draw()
        CMS_label.Draw()
        canvas.Print('plots/combined/%s_%s.eps'%(vname,wname))

vars_for_ROC = []
vars_for_ROC.append('PSE'         )
vars_for_ROC.append('PSEOverEt'   )
vars_for_ROC.append('PSEOverE'    )
vars_for_ROC.append('PSEOverEz'   )
vars_for_ROC.append('sixix'       )
vars_for_ROC.append('siyiy'       )
vars_for_ROC.append('sirir'       )
vars_for_ROC.append('sixixOSiyiy' )
vars_for_ROC.append('sixixOSirir' )
vars_for_ROC.append('siyiyOSirir' )
vars_for_ROC.append('sixixMSiyiy' )
vars_for_ROC.append('ps_ix0'      )
vars_for_ROC.append('ps_iy0'      )
vars_for_ROC.append('ps_ix'       )
vars_for_ROC.append('ps_iy'       )
vars_for_ROC.append('ps_ir'       )
vars_for_ROC.append('ps_ixy'      )
vars_for_ROC.append('rxy'         )
vars_for_ROC.append('r9'          )
vars_for_ROC.append('fBrem'       )

canvas.SetLogy(ROOT.kFALSE)
for vname in vars_for_ROC:
    mg = ROOT.TMultiGraph('mg_%s'%vname, '')
    graphs = {}
    legend = ROOT.TLegend(0.5,0.5,0.9,0.2)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetShadowColor(0)
    
    for wname in weight_names:
        h_ZprimeM1000 = f.Get('h_%s_ZprimeToEE_M1000_v5_%s'%(vname,wname)).Clone('h_ZprimeM1000')
        h_QCD         = f.Get('h_%s_QCD_v5_%s'             %(vname,wname)).Clone('h_QCD'        )
        
        eff_sig = []
        eff_bkg = []
        if vname=='ps_ix0' or vname=='ps_iy0':
            for bin in range(1,(h_QCD.GetNbinsX()+1)/2):
                b1 = bin
                b2 = h_QCD.GetNbinsX()+1-bin
                es = h_ZprimeM1000.Integral(b1,b2)/h_ZprimeM1000.GetSumOfWeights()
                eb =         h_QCD.Integral(b1,b2)/h_QCD.GetSumOfWeights()
                eff_sig.append(es)
                eff_bkg.append(eb)
        else:
            for bin in range(1,h_QCD.GetNbinsX()+1):
                es = h_ZprimeM1000.Integral(1,bin)/h_ZprimeM1000.GetSumOfWeights()
                eb =         h_QCD.Integral(1,bin)/h_QCD.GetSumOfWeights()
                eff_sig.append(es)
                eff_bkg.append(eb)
        
        arr_eff_sig = numpy.array(eff_sig, 'd')
        arr_eff_bkg = numpy.array(eff_bkg, 'd')
        n = len(eff_sig)
        
        graphs[wname] = ROOT.TGraph(n, arr_eff_bkg, arr_eff_sig)
        graphs[wname].GetXaxis().SetTitle('background efficiency')
        graphs[wname].GetYaxis().SetTitle('signal efficiency'    )
        graphs[wname].SetMarkerStyle(20)
        graphs[wname].GetXaxis().SetTitleOffset(1.25)
        graphs[wname].GetYaxis().SetTitleOffset(1.25)
        graphs[wname].SetMarkerStyle(weight_markers[wname])
        graphs[wname].SetMarkerColor(weight_colors[wname])
        graphs[wname].SetLineColor(weight_colors[wname])
        
        legend.AddEntry(graphs[wname], weight_titles[wname], 'pl')
        
        mg.Add(graphs[wname])
    
    mg.Draw('ALP')
    mg.GetXaxis().SetTitle('QCD efficiency')
    mg.GetYaxis().SetTitle('Z\'(1000)#rightarrowee efficiency')
    mg.GetXaxis().SetTitleOffset(1.25)
    mg.GetYaxis().SetTitleOffset(1.25)
    mg.GetXaxis().SetLabelSize(0.04)
    mg.GetYaxis().SetLabelSize(0.04)
    mg.Draw('ALP')
    legend.Draw()
    
    canvas.Print('plots/combined/ROC/%s.eps'%(vname))
