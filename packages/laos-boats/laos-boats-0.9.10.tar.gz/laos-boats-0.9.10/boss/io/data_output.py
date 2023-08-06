import numpy as np
import os

from . import IOutils

class DataOutput:
    """
    Functionality to output raw data on request to files outside of the main
    output (*.out) file and the restart (*.rst) file.
    """

    @staticmethod
    def dump_model(STS, dest_file, bo, mod_params, xhat):
        """
        Dumps model slice (up to 2D) mean and variance in a grid to
        models/it#.dat
        """
        model_data = np.array([[]]*(STS.dim + 2)) # coords + mu + nu
        npts = STS.pp_m_slice[2]
        coords = np.array([
            np.linspace(STS.bounds[i,0], STS.bounds[i,1], npts)
            for i in STS.pp_m_slice[:2]
                         ])
        defaults = xhat if STS.pp_x_defaults is None else STS.pp_x_defaults
        if STS.pp_m_slice[0] != STS.pp_m_slice[1]:
            # 2D slice
            x1, x2 = np.meshgrid(coords[0], coords[1])
            for i in range(npts):
                for j in range(npts):
                    p = np.array([x1[i,j], x2[i,j]])
                    for d in range(STS.dim):
                        if d not in STS.pp_m_slice[:2]:
                            p = np.insert(p, d, defaults[d])
                    p = np.insert(p, len(p), float(bo.get_mu(p)))
                    p = np.insert(p, len(p), float(bo.get_nu(p)))
                    model_data = np.insert(model_data,
                                 len(model_data[0]), p, axis=1)
            titleLine = "Model dump (x mu nu)" \
                        + ", grid of %ix%i=%i pts"%(npts,npts,npts**2)
        else:
            # 1D slice
            x1 = coords[0]
            for i in range(npts):
                p = np.array([x1[i]])
                for d in range(STS.dim):
                    if d not in STS.pp_m_slice[:2]:
                        p = np.insert(p, d, defaults[d])
                p = np.insert(p, len(p), float(bo.get_mu(p)))
                p = np.insert(p, len(p), float(bo.get_nu(p)))
                model_data = np.insert(model_data,
                             len(model_data[0]), p, axis=1)
            titleLine = "Model dump (x mu nu)" \
                        + ", grid of %i pts"%(npts)


        titleLine += "\nModel parameter values (noise variance lengthscales " \
                     + "[periods]): " + str(mod_params)
        IOutils.writeCols(dest_file,
                    model_data, '    ', titleLine, '%18.8E')

    @staticmethod
    def dump_acqfn(STS, dest_file, bo, acqfn, defs):
        """
        Dumps acquisition function slice (up to 2D) in a grid to
        acqfns/it#.dat
        """
        acqf_data = [[]]*(STS.dim + 1) # coords + acqf
        npts = STS.pp_m_slice[2]
        coords = np.array([
            np.linspace(STS.bounds[i,0], STS.bounds[i,1], npts)
            for i in STS.pp_m_slice[:2]
                         ])
        defaults = defs if STS.pp_x_defaults is None else STS.pp_x_defaults
        if STS.pp_m_slice[0] != STS.pp_m_slice[1]:
            # 2D slice
            x1, x2= np.meshgrid(coords[0], coords[1])
            for i in range(npts):
                for j in range(npts):
                    p = np.array([x1[i,j], x2[i,j]])
                    for d in range(STS.dim):
                        if d not in STS.pp_m_slice[:2]:
                            p = np.insert(p, d, defaults[d])
                    af, daf = acqfn(p, bo.model, bo.acqfnpars)
                    p = np.insert(p, len(p), float(af))
                    acqf_data = np.insert(acqf_data,
                                 len(acqf_data[0]), p, axis=1)
            titleLine = "Acquisition function dump (x" \
                        + " af), grid of %i pts"%(npts**2)
        else:
            # 1D slice
            x1 = coords[0]
            for i in range(npts):
                p = np.array([x1[i]])
                for d in range(STS.dim):
                    if d not in STS.pp_m_slice[:2]:
                        p = np.insert(p, d, defaults[d])
                af, daf = acqfn(p, bo.model, bo.acqfnpars)
                p = np.insert(p, len(p), float(af))
                acqf_data = np.insert(acqf_data,
                             len(acqf_data[0]), p, axis=1)
            titleLine = "Acquisition function dump (x" \
                        + " af), grid of %i pts"%(npts)

        IOutils.writeCols(dest_file, acqf_data,'    ', titleLine, '%18.8E')


    @staticmethod
    def dump_truef(STS, dest_file, last_xhat):
        """
        Dumps true function slice (up to 2D) in a grid
        """
        truef_data = [[]]*(STS.dim + 1) # coords + truef
        npts = STS.pp_truef_npts
        coords = np.array([
            np.linspace(STS.bounds[i,0], STS.bounds[i,1], npts)
            for i in STS.pp_m_slice[:2]
                         ])
        defaults = last_xhat if STS.pp_x_defaults is None else STS.pp_x_defaults
        if STS.pp_m_slice[0] != STS.pp_m_slice[1]:
            # 2D slice
            x1, x2= np.meshgrid(coords[0], coords[1])
            for i in range(npts):
                for j in range(npts):
                    p = np.array([x1[i,j], x2[i,j]])
                    for d in range(STS.dim):
                        if d not in STS.pp_m_slice[:2]:
                            p = np.insert(p, d, defaults[d])
                    tf = STS.f(np.atleast_2d(p))
                    os.chdir(STS.dir)
                    p = np.insert(p, len(p), float(tf))
                    truef_data = np.insert(truef_data,
                                 len(truef_data[0]), p, axis=1)
            titleLine = "True function dump (x"\
                        + " f), grid of %ix%i=%i pts"%(npts,npts,npts**2)
        else:
            # 1D slice
            x1 = coords[0]
            for i in range(npts):
                p = np.array([x1[i]])
                for d in range(STS.dim):
                    if d not in STS.pp_m_slice[:2]:
                        p = np.insert(p, d, defaults[d])
                tf = STS.f(np.atleast_2d(p))
                os.chdir(STS.dir)
                p = np.insert(p, len(p), float(tf))
                truef_data = np.insert(truef_data,
                             len(truef_data[0]), p, axis=1)
            titleLine = "True function dump (x" \
                        + " f), grid of %i pts"%(npts)

        IOutils.writeCols(dest_file, truef_data,'    ',
                                        titleLine, '%18.8E')


