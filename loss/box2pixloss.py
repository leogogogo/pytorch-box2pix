import torch
import torch.nn as nn


class Box2PixLoss(nn.Module):
    def __init__(self):
        super(Box2PixLoss, self).__init__()

        self.uncert_semantics = nn.Parameter(torch.Tensor(1))
        self.uncert_offsets = nn.Parameter(torch.Tensor(1))
        self.uncert_ssdbox = nn.Parameter(torch.Tensor(1))
        self.uncert_ssdclass = nn.Parameter(torch.Tensor(1))

        for p in self.parameters():
            nn.init.zeros_(p)

    def forward(self, semantics_loss, offsets_loss, box_loss, conf_loss):
        loss1 = torch.exp(-0.5 * self.uncert_semantics) * semantics_loss + self.uncert_semantics
        loss2 = torch.exp(-self.uncert_offsets) * offsets_loss + self.uncert_offsets
        loss3 = torch.exp(-self.uncert_ssdbox) * box_loss + self.uncert_ssdbox
        loss4 = torch.exp(-0.5 * self.uncert_ssdclass) * conf_loss + self.uncert_ssdclass

        loss = loss1 + loss2 + loss3 + loss4

        return loss