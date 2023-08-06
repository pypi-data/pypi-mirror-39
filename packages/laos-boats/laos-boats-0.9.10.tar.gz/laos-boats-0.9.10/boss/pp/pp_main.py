import warnings; warnings.filterwarnings("ignore") # ignore warnings
import os
import numpy as np

from ..bo import BoMain, Model
from ..io import Parse, DataOutput, IOutils
from .plot import Plot
from ..utils import Minimization

def _recreate_bo(STS, acqs, par, mainOutput):
    """
    Loads given data and parameters to a given model object
    """
    dim = STS.dim
    X = acqs[:,:dim]
    Y = acqs[:, dim:dim+1]
    bo = BoMain(STS, mainOutput, None)
    bo.add_xy_list(X, Y)
    bo.model.set_unfixed_params(par)
    return(bo)

def _find_index(array, npts):
        if array.size == 0:
            return None
        else:
            ind = np.where(array[:,0] == npts)[0]
            if ind.size == 0:
                return None
            else:
                return ind[0]


def PPmain(STS, ipt_rstfile, ipt_outfile, mainOutput):
    """
    Controls all the post-processing features
    """
    # create needed directories
    if os.path.isdir('postprocessing'):
        print("warning: overwriting directory 'postprocessing'")
    os.system('rm -rf postprocessing')
    os.system('mkdir -p postprocessing')
    os.system('mkdir -p postprocessing/bo_data')
    os.system('mkdir -p postprocessing/bo_graphs')
    if STS.pp_models:
        os.system('mkdir -p postprocessing/bo_data/models')
        os.system('mkdir -p postprocessing/bo_graphs/models')
    if STS.pp_acqfs:
        os.system('mkdir -p postprocessing/bo_data/acqfns')
        os.system('mkdir -p postprocessing/bo_graphs/acqfns')
    if STS.pp_local_mins is not None:
        os.system('mkdir -p postprocessing/bo_data/local_minima')

    # parse data to use
    acqs, mod_par = Parse.rst(STS, ipt_rstfile)
    min_preds = Parse.min_preds(STS, ipt_outfile)
    best_acqs = Parse.best_acqs(STS, ipt_outfile)
    conv_meas = Parse.conv_measures(STS, ipt_outfile)
    xnexts = Parse.xnexts(STS, ipt_outfile)
    est_yranges = np.array([[acqs[i-1,0],max(acqs[:i,-1])-min(acqs[:i,-1])] for i in range(1,len(acqs)+1)])

    # initialize dump files
    acqs_file = "postprocessing/bo_data/acquisitions.dat"
    IOutils.overwrite(acqs_file, "Data acquisitions "
                              + "by iteration (iter npts x y)\n")
    min_pred_file = "postprocessing/bo_data/minimum_predictions.dat"
    IOutils.overwrite(min_pred_file, "Global minimum predictions by iteration"
                              + " (iter npts x_hat mu_hat nu_hat)\n")
    conv_meas_file = "postprocessing/bo_data/convergence_measures.dat"
    IOutils.overwrite(conv_meas_file, "Convergence measures by iteration"
                              + " (iter npts abs(dx_hat) abs(dmu_hat)/yrange)\n")
    hypers_file = "postprocessing/bo_data/hyperparameters.dat"
    IOutils.overwrite(hypers_file,"Model hyperparameter values by iteration"
                              + " (iter npts variance lengthscales)\n")
    if STS.pp_true_hats:
        truehat_file = "postprocessing/bo_data/true_f_at_x_hat.dat"
        IOutils.overwrite(truehat_file,"True function value at x_hat locations"
                                  + " by iteration (iter npts f(x_hat) "
                                  +"f(x_hat)-mu_hat)\n")


    # recreate snapshots of model in a loop for all pp_iters and dump data
    slc_dim = 1 if STS.pp_m_slice[0] == STS.pp_m_slice[1] else 2
    curr_xhat = None
    for it in STS.pp_iters:
        npts = STS.initpts + it
        ind_acqs = _find_index(acqs, npts)
        ind_par = _find_index(mod_par, npts)
        if ind_acqs is None or ind_par is None:
            mainOutput.progress_msg("Could not find data or "
               + " parameters to recreate model at iteration %i,"%(it)
               + " skipping post-processing for that iteration.", 0)
        else:
            mainOutput.progress_msg("Post-processing iteration %i"%(it),1)
            bo = _recreate_bo(STS,
                              acqs[:ind_acqs+1,1:],
                              mod_par[ind_par,1:],
                              mainOutput,
            )
            assert (npts == bo.model.X.shape[0]), "Model recreated wrong!"

            # acquisitions
            IOutils.append_write(acqs_file,
                    IOutils.data_line([it, npts], acqs[ind_acqs,1:],
                                      fstr="%18.10E"
                    )
            )

            # global minimum predictions
            ind_mp = _find_index(min_preds, npts)
            if ind_mp is not None:
                IOutils.append_write(min_pred_file,
                        IOutils.data_line([it, npts], min_preds[ind_mp,1:],
                                          fstr="%18.10E"
                        )
                )
                curr_xhat = min_preds[ind_mp,1:STS.dim+1]

            # convergence measures
            ind_cm = _find_index(conv_meas, npts)
            if ind_cm is not None:
                IOutils.append_write(conv_meas_file,
                    IOutils.data_line([it, npts,
                    conv_meas[ind_cm,-2],
                    conv_meas[ind_cm,-1]],
                    fstr="%18.10E"
                        )
                )

            # hyperparameters
            IOutils.append_write(hypers_file,
                    IOutils.data_line([it, npts], mod_par[ind_par,1:],
                                      fstr="%18.10E"
                    )
            )

            # true function at xhat
            if STS.pp_true_hats and ind_mp is not None:
                mainOutput.progress_msg("Evaluating true function at x_hat",2)
                tfhat = STS.f(np.atleast_2d(min_preds[ind_mp,1:STS.dim+1]))
                muhat = min_preds[ind_mp,-2]
                IOutils.append_write(truehat_file,
                    IOutils.data_line([it, npts, tfhat, tfhat-muhat],
                                      fstr="%18.10E"
                    )
                )

            # local minima
            if STS.pp_local_mins is not None:
                mainOutput.progress_msg("Finding model local minima",2)
                mins = Minimization.minimize(bo.model.mu_with_grad, STS.bounds,
                        np.hstack([bo.get_x(), bo.get_y()]), STS.min_dist_acqs,
                        accuracy=STS.pp_local_mins, args=(),
                        lowest_min_only=False)
                mins = sorted(mins, key=lambda x:(x[1]))
                minima_data = [[]] * (STS.dim + 1)
                for m in mins:
                    p = []
                    for i in range(STS.dim):
                        p.append(m[0][i])
                    p.append(m[1])
                    minima_data = np.insert(minima_data, len(minima_data[0]),
                                            p, axis=1)
                titleLine = "Local minima (x y) - model data ensemble size %i"\
                                                         %(npts)
                IOutils.writeCols("postprocessing/bo_data/local_minima/"\
                            "it%.4i_npts%.4i.dat"%(it,npts), minima_data,
                            titleLine=titleLine)

            # model (cross-sections)
            if STS.pp_models:
                DataOutput.dump_model(STS,
                    'postprocessing/bo_data/models/it%.4i_npts%.4i.dat'\
                    %(it,npts), bo, bo.model.get_all_params(),
                    curr_xhat)
                mdata = IOutils.readCols('postprocessing/bo_data/models/'
                                         + 'it%.4i_npts%.4i.dat'%(it,npts),
                                         skiprows=2)
                if ind_mp is not None:
                    xhat = min_preds[ind_mp,1:STS.dim+1]
                else: xhat = None
                macqs = acqs[:ind_acqs+1,1:]
                if slc_dim < STS.dim and slc_dim == 1: macqs = None
                ind_xnext = _find_index(xnexts, npts)
                if ind_xnext is not None and slc_dim == STS.dim:
                    xnext = xnexts[ind_xnext,1:]
                else: xnext = None
                if STS.pp_local_mins is not None and slc_dim == STS.dim:
                    minima = np.atleast_2d(np.array(minima_data)).T
                else: minima = None

                Plot.model(STS, 'postprocessing/bo_graphs/models/it%.4i_npts%.4i'\
                    '.png'%(it,npts), mdata, xhat, macqs, xnext, minima)


            # acquisition function (cross-sections)
            if STS.pp_acqfs and it >= 0:
                ind_xnext = _find_index(xnexts, npts)
                if ind_xnext is not None:
                    defs = xnexts[ind_xnext,1:]
                else: defs = curr_xhat
                xn, acqfn = bo._acqnext(it)
                DataOutput.dump_acqfn(
                     STS,'postprocessing/bo_data/acqfns/it%.4i_npts%.4i.dat'\
                     %(it,npts), bo, acqfn, defs)
                acqfn_data = IOutils.readCols('postprocessing/bo_data/acqfns/'
                                         + 'it%.4i_npts%.4i.dat'%(it,npts))
                if ind_mp is not None and slc_dim == STS.dim:
                    xhat = min_preds[ind_mp,1:STS.dim+1]
                else: xhat = None
                macqs = acqs[:ind_acqs+1,1:] if slc_dim == 2 else None
                ind_xnext = _find_index(xnexts, npts)
                if ind_xnext is not None:
                    xnext = xnexts[ind_xnext,1:]
                else: xnext = None

                Plot.acq_func(STS, 'postprocessing/bo_graphs/acqfns/'\
                  'it%.4i_npts%.4i.png'%(it,npts), acqfn_data, macqs, xhat, xnext)


    # plot all quantities as a function of iteration
    acqs_data = np.atleast_2d(IOutils.readCols(acqs_file))
    minp = np.atleast_2d(IOutils.readCols(min_pred_file))
    if len(minp[0]) == 0:
        raise ValueError('No minimal points found in out-file.')
    diff = np.where(acqs_data[:,0] == minp[0,0])[0]
    if diff.size > 0:
        acqs_data = acqs_data[diff[0]:]
        if len(acqs_data) > 1:
            Plot.data_acquisitions(STS, "postprocessing/bo_graphs/acquisition"
                                    + "_locations.png", acqs_data, minp)

    conv_meas = np.atleast_2d(IOutils.readCols(conv_meas_file))
    if len(conv_meas) > 1:
        Plot.conv_measures(STS, "postprocessing/bo_graphs/convergence_measures.png",
                            conv_meas)

    hypers = np.atleast_2d(IOutils.readCols(hypers_file))
    if len(hypers) > 1:
        Plot.hyperparameters(STS, "postprocessing/bo_graphs/hyperparameters.png",
                            hypers)

    if STS.pp_true_hats:
        truef_hats = np.atleast_2d(IOutils.readCols(truehat_file))
        if len(truef_hats) > 1:
            Plot.truef_hat(STS, "postprocessing/bo_graphs/true_function"
                                 + "_at_xhats.png", truef_hats)




    # dump and plot true function (cross-section)
    if STS.pp_truef_npts:
        mainOutput.progress_msg("Dumping and plotting true function", 1)
        if curr_xhat is None: curr_xhat = min_preds[-1,1:STS.dim+1]
        DataOutput.dump_truef(STS, 'postprocessing/bo_data/true_func.dat',
            curr_xhat)
        truef_data = IOutils.readCols("postprocessing"
                                                 + "/bo_data/true_func.dat")
        Plot.truef(STS, "postprocessing/bo_graphs/true_func.png", truef_data)
        ind = np.where(min_preds[:,1:STS.dim+1] == curr_xhat)[0][0]
        truef_slc_xhat_npts = int(min_preds[ind,0])


        # replot 1D models with truef if it is now available
        if STS.pp_m_slice[0] == STS.pp_m_slice[1] and STS.pp_models:
            mainOutput.progress_msg("Replotting 1D models with true"
                                         + " function", 1)
            for mdat_file in os.listdir("postprocessing/bo_data/models"):
                # find it and and npts from naming it%.4i_npts%.4i.dat
                negit = True if mdat_file[2] == '-' else False
                it   = int(mdat_file[2:6]) if not negit else int(mdat_file[2:7])
                npts = int(mdat_file[-8:-4])
                mdata = IOutils.readCols('postprocessing/bo_data/models/'
                           + 'it%.4i_npts%.4i.dat'%(it,npts), skiprows=2)
                ind_mp = _find_index(min_preds, npts)
                if ind_mp is not None:
                    xhat = min_preds[ind_mp,1:STS.dim+1]
                else: xhat = None
                ind_acqs = _find_index(acqs, npts)
                macqs = acqs[:ind_acqs+1,1:]
                if slc_dim < STS.dim and slc_dim == 1: macqs = None
                ind_xnext = _find_index(xnexts, npts)
                if ind_xnext is not None and slc_dim == STS.dim:
                    xnext = xnexts[ind_xnext,1:]
                else: xnext = None

                if STS.pp_local_mins is not None and slc_dim == STS.dim:
                    minima = IOutils.readCols("postprocessing/bo_data/local_"\
                        + "minima/it%.4i_npts%.4i.dat"%(it,npts))
                    minima = np.atleast_2d(minima)
                else: minima = None

                if npts != truef_slc_xhat_npts and slc_dim < STS.dim:
                    truef_d = None
                else: truef_d = truef_data

                Plot.model(STS, 'postprocessing/bo_graphs/models/'
                    + 'it%.4i_npts%.4i.png'%(it,npts), mdata, xhat, macqs,
                            xnext, minima, truef_d)









