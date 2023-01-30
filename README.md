# Generovanie syntetických 2D obrázkov a 3D dát pre inštančnú segmentáciu a analýza zubov použitím techník hlbokého učenia

## Popis diplomovej práce
Častým problémom pri trénovaní modelov v oblasti medicíny je nedostatočné množstvo dát. V tejto práci som sa preto rozhodla venovať generovaniu syntetických dát presnejšie generovaniu obrázkov ľudského chrupu z rôznych pohľadov za pomoci neurónových sietí.

## Ciele práce
- naštudovanie relevantnej literatúry
- získanie dát na trénovanie neurónovej siete
- vytvorenie modelu na generovanie syntetických 2D obrázkov chrupu
- analýza zubov použitím techník hlbokého učenia

## Naštudovaná literatúra
- [Intraoral image generation by progressive growing of generative adversarial network and evaluation of generated image quality by dentists](https://www.nature.com/articles/s41598-021-98043-3)
- [A Style-Based Generator Architecture for Generative Adversarial Networks](https://arxiv.org/pdf/1812.04948.pdf)
- [Conditional Generative Adversarial Nets](https://arxiv.org/pdf/1411.1784.pdf%EF%BC%88CGAN%EF%BC%89)
- [Mapping intraoral photographs on virtual teeth model](https://www.sciencedirect.com/science/article/abs/pii/S0300571218302781?casa_token=wBOaNKhLohYAAAAA:fEwUNoLiFeKO_0834-y7hmNegzvcDlB0_tLQPNfZnJph0FTZeWgsLQQ2bxI6_NriEHiq9oWKmw)
- [Tooth Numbering and Condition Recognition on Dental Panoramic Radiograph Images Using CNNs](https://ieeexplore.ieee.org/abstract/document/9652543)
- [TSegNet: An efficient and accurate tooth segmentation network on 3D dental model](https://www.sciencedirect.com/science/article/abs/pii/S1361841520303133?casa_token=sfJy78D3uWsAAAAA:O80xxmJ4YvLEJpGrLzJZVu1g6lgFPKOVP-UU2VLh84vQwDZXfB1lgIuNdjXfmDwaWDgfUurKGWQ)
- [Detection of dental caries in oral photographs taken by mobile phones based on the YOLOv3 algorithm](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8640896/)

## Praktická práca
- nainštalovanie potrebného softvéru
- napísanie [skriptu](scripts/download_images.py) na automatizované sťahovanie fotiek chrupu z webovej stránky spoločnosti Invisalign
- [predspracovanie](scripts/data_preprocessing.py) fotiek pre účely trénovania siete
- [implementácia GAN siete](scripts/train_gan_blackwhite.py) s jednoduchou architektúrou na generovanie šedoúrovňových fotiek frontálneho úseku chrupu
- [implementácia DCGAN siete](scripts/train_gan_rgb.py) s jednoduchou architektúrou na generovanie farebných fotiek frontálneho úseku chrupu


## Reprodukcia výsledkov

**Predpokladom je nainštalovaný `python3`**

1. Vytvorenie virtuálneho prostredia
```
python -m venv venv
source venv/bin/activate
```

2. Inštalácia balíčkov

```
pip install -r requirements.txt
```