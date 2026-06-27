import torch
import torch.nn as nn
from einops import rearrange

# ==========================================
# 1. 기본 부품 (Conv Block)
# ==========================================
class ConvBlock(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        return self.conv(x)

# ==========================================
# 2. 트랜스포머 블록 (Transformer Block) - 핵심!
# ==========================================
class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        # Multi-Head Attention
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.norm1 = nn.LayerNorm(embed_dim)
        
        # Feed Forward Network
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Linear(embed_dim * 4, embed_dim)
        )
        self.norm2 = nn.LayerNorm(embed_dim)

    def forward(self, x):
        # x shape: (Sequence_len, Batch, Embed_dim)
        # 1. Self-Attention + Residual
        attn_out, _ = self.attention(x, x, x)
        x = x + self.norm1(attn_out)
        
        # 2. MLP + Residual
        mlp_out = self.mlp(x)
        x = x + self.norm2(mlp_out)
        return x

# ==========================================
# 3. TransUNet 전체 구조
# ==========================================
class TransUNet(nn.Module):
    def __init__(self, img_dim=256, in_channels=3, out_channels=1, head_num=4, mlp_dim=512, block_num=4, patch_dim=16):
        super().__init__()
        self.img_dim = img_dim
        self.patch_dim = patch_dim
        
        # ---------------------------
        # Encoder (CNN Part) - 내려가는 길
        # ---------------------------
        self.enc1 = ConvBlock(in_channels, 64)
        self.pool1 = nn.MaxPool2d(2) # 256 -> 128
        
        self.enc2 = ConvBlock(64, 128)
        self.pool2 = nn.MaxPool2d(2) # 128 -> 64
        
        self.enc3 = ConvBlock(128, 256)
        self.pool3 = nn.MaxPool2d(2) # 64 -> 32

        # ---------------------------
        # Bottleneck (Transformer Part) - 핵심!
        # ---------------------------
        # CNN에서 나온 32x32 이미지를 패치(조각)로 만듭니다.
        self.embedding_dim = 256
        self.transformer_blocks = nn.ModuleList(
            [TransformerBlock(self.embedding_dim, head_num) for _ in range(block_num)]
        )
        
        # ---------------------------
        # Decoder (CNN Part) - 올라가는 길
        # ---------------------------
        self.up3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec3 = ConvBlock(256, 128) # skip connection (128+128)
        
        self.up2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec2 = ConvBlock(128, 64)
        
        self.up1 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.dec1 = ConvBlock(96, 32) # 64(enc1) + 32(up1) = 96
        
        self.final = nn.Conv2d(32, out_channels, kernel_size=1)

    def forward(self, x):
        # [Encoder]
        e1 = self.enc1(x)       # 256x256
        p1 = self.pool1(e1)
        
        e2 = self.enc2(p1)      # 128x128
        p2 = self.pool2(e2)
        
        e3 = self.enc3(p2)      # 64x64
        p3 = self.pool3(e3)     # 32x32 (채널 256)

        # [Transformer Bottleneck]
        # 1. 이미지를 일렬로 폄 (Flatten): (Batch, Channel, H, W) -> (H*W, Batch, Channel)
        # Transformer는 이미지가 아니라 '시퀀스(문장)'를 원하니까요.
        b, c, h, w = p3.shape
        embedding = rearrange(p3, 'b c h w -> (h w) b c')
        
        # 2. 트랜스포머 통과 (문맥 파악)
        for block in self.transformer_blocks:
            embedding = block(embedding)
            
        # 3. 다시 이미지 형태로 복구
        encoded = rearrange(embedding, '(h w) b c -> b c h w', h=h, w=w)
        
        # [Decoder] U-Net과 동일
        d3 = self.up3(encoded)     # 32 -> 64
        d3 = torch.cat((e2, d3), dim=1) # Skip Connection
        d3 = self.dec3(d3)
        
        d2 = self.up2(d3)          # 64 -> 128
        d2 = torch.cat((e1, d2), dim=1)
        d2 = self.dec2(d2)
        
        d1 = self.up1(d2)          # 128 -> 256
        # 여기서는 크기 차이 때문에 e1을 안 쓰고 간단히 처리하거나, e1을 맞춰서 씁니다.
        # 이번 구현에선 e1과 결합
        d1 = torch.cat((e1, d1), dim=1) 
        d1 = self.dec1(d1)
        
        return self.final(d1)