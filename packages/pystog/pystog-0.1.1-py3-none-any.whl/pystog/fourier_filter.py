# import modules
from __future__ import (absolute_import, division, print_function)

from pystog.converter import Converter
from pystog.transformer import Transformer


class FourierFilter(object):
    def __init__(self):
        self.converter = Converter()
        self.transformer = Transformer()

    # g(r)
    def g_using_F(self, r, gr, q, fq, cutoff, **kwargs):
        # setup qmin, qmax, and get low-r region to back transform
        qmin = min(q)
        qmax = max(q)
        r_tmp, gr_tmp_initial = self.transformer.apply_cropping(
            r, gr, 0.0, cutoff)

        # Shift low-r so it goes to 1 at "high-r" for this section. Reduces the
        # sinc function issue.
        gr_tmp = gr_tmp_initial + 1

        # Transform the shifted low-r region to F(Q) to get F(Q)_ft
        q_ft = self.transformer._extend_axis_to_low_end(q)
        q_ft, fq_ft = self.transformer.g_to_F(r_tmp, gr_tmp, q_ft, **kwargs)
        q_ft, fq_ft = self.transformer.apply_cropping(q_ft, fq_ft, qmin, qmax)

        # Subtract F(Q)_ft from original F(Q) = delta_F(Q)
        q, fq = self.transformer.apply_cropping(q, fq, qmin, qmax)
        fq = (fq - fq_ft)

        # Transform delta_F(Q) for g(r) with low-r removed
        r, gr = self.transformer.F_to_g(q, fq, r, **kwargs)

        return q_ft, fq_ft, q, fq, r, gr

    def g_using_S(self, r, gr, q, sq, cutoff, **kwargs):
        fq = self.converter.S_to_F(q, sq)
        q_ft, fq_ft, q, fq, r, gr = self.g_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        sq_ft = self.converter.F_to_S(q_ft, fq_ft)
        sq = self.converter.F_to_S(q, fq)
        return q_ft, sq_ft, q, sq, r, gr

    def g_using_FK(self, r, gr, q, fq, cutoff, **kwargs):
        fq = self.converter.FK_to_F(q, fq)
        q_ft, fq_ft, q, fq, r, gr = self.g_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        fq_ft = self.converter.F_to_FK(q_ft, fq_ft)
        fq = self.converter.F_to_FK(q, fq)
        return q_ft, fq_ft, q, fq, r, gr

    def g_using_DCS(self, r, gr, q, dcs, cutoff, **kwargs):
        fq = self.converter.DCS_to_F(q, dcs)
        q_ft, fq_ft, q, fq, r, gr = self.g_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        dcs_ft = self.converter.F_to_DCS(q_ft, fq_ft)
        dcs = self.converter.F_to_DCS(q_ft, fq)
        return q_ft, dcs_ft, q, dcs, r, gr

    # G(R) = PDF
    def G_using_F(self, r, gr, q, fq, cutoff, **kwargs):
        gr = self.converter.G_to_g(r, gr, **kwargs)
        q_ft, fq_ft, q, fq, r, gr = self.g_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        gr = self.converter.g_to_G(r, gr, **kwargs)
        return q_ft, fq_ft, q, fq, r, gr

    def G_using_S(self, r, gr, q, sq, cutoff, **kwargs):
        fq = self.converter.S_to_F(q, sq)
        q_ft, fq_ft, q, fq, r, gr = self.G_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        sq_ft = self.converter.F_to_S(q_ft, fq_ft)
        sq = self.converter.F_to_S(q, fq)
        return q_ft, sq_ft, q, sq, r, gr

    def G_using_FK(self, r, gr, q, fq, cutoff, **kwargs):
        fq = self.converter.FK_to_F(q, fq, **kwargs)
        q_ft, fq_ft, q, fq, r, gr = self.G_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        fq_ft = self.converter.F_to_FK(q_ft, fq_ft, **kwargs)
        fq = self.converter.F_to_FK(q, fq, **kwargs)
        return q_ft, fq_ft, q, fq, r, gr

    def G_using_DCS(self, r, gr, q, dcs, cutoff, **kwargs):
        fq = self.converter.DCS_to_F(q, dcs, **kwargs)
        q_ft, fq_ft, q, fq, r, gr = self.G_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        dcs_ft = self.converter.F_to_DCS(q_ft, fq_ft, **kwargs)
        dcs = self.converter.F_to_DCS(q, fq, **kwargs)
        return q_ft, dcs_ft, q, dcs, r, gr

    # Keen's G(r)
    def GK_using_F(self, r, gr, q, fq, cutoff, **kwargs):
        gr = self.converter.GK_to_g(r, gr, **kwargs)
        q_ft, fq_ft, q, fq, r, gr = self.g_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        gr = self.converter.g_to_GK(r, gr, **kwargs)
        return q_ft, fq_ft, q, fq, r, gr

    def GK_using_S(self, r, gr, q, sq, cutoff, **kwargs):
        fq = self.converter.S_to_F(q, sq)
        q_ft, fq_ft, q, fq, r, gr = self.GK_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        sq_ft = self.converter.F_to_S(q_ft, fq_ft)
        sq = self.converter.F_to_S(q, fq)
        return q_ft, sq_ft, q, sq, r, gr

    def GK_using_FK(self, r, gr, q, fq, cutoff, **kwargs):
        fq = self.converter.FK_to_F(q, fq)
        q_ft, fq_ft, q, fq, r, gr = self.GK_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        fq_ft = self.converter.F_to_FK(q_ft, fq_ft, **kwargs)
        fq = self.converter.F_to_FK(q, fq, **kwargs)
        return q_ft, fq_ft, q, fq, r, gr

    def GK_using_DCS(self, r, gr, q, dcs, cutoff, **kwargs):
        fq = self.converter.DCS_to_F(q, dcs, **kwargs)
        q_ft, fq_ft, q, fq, r, gr = self.GK_using_F(
            r, gr, q, fq, cutoff, **kwargs)
        dcs_ft = self.converter.F_to_DCS(q_ft, fq_ft, **kwargs)
        dcs = self.converter.F_to_DCS(q, fq, **kwargs)
        return q_ft, dcs_ft, q, dcs, r, gr
