function out = coreg_spm_m(imref, imflo, costfun, sep, tol, fwhm, params, graphics, visual)

    if visual>0
        Fgraph = spm_figure('GetWin','Graphics');
        Finter = spm_figure('GetWin','Interactive');
    end

    cflags.cost_fun = costfun;
    cflags.sep = sep;
    cflags.tol = tol;
    cflags.fwhm = fwhm;
    cflags.params = params;
    cflags.graphics = graphics;

    VG = strcat(imref,',1');
    VF = strcat(imflo,',1');
    disp(imref);
    disp(imflo);
    disp(cflags)
    disp(tol)

    spm_jobman('initcfg')

    x = spm_coreg(VG,VF,cflags);
    M = spm_matrix(x);

    out = M;
end