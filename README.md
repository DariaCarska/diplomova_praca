# Generovanie syntetických 2D obrázkov zubov

## Popis diplomovej práce
Častým problémom pri trénovaní modelov v oblasti medicíny je nedostatočné množstvo dát. V tejto práci som sa preto rozhodla venovať generovaniu syntetických dát presnejšie generovaniu obrázkov ľudského chrupu z rôznych pohľadov za pomoci neurónových sietí.

## Ciele práce
- naštudovanie relevantnej literatúry
- získanie dát na trénovanie neurónovej siete
- trénovanie modelov na generovanie syntetických 2D obrázkov chrupu

## Naštudovaná literatúra
- [Intraoral image generation by progressive growing of generative adversarial network and evaluation of generated image quality by dentists](https://www.nature.com/articles/s41598-021-98043-3)
- [Progressive Growing of GANs for Improved Quality, Stability, and Variation](https://arxiv.org/pdf/1710.10196.pdf)
- [A Style-Based Generator Architecture for Generative Adversarial Networks](https://arxiv.org/pdf/1812.04948.pdf)
- [Generative Adversarial Transformers](https://arxiv.org/pdf/2103.01209.pdf)


## Praktická práca
- nainštalovanie potrebného softvéru
- napísanie [skriptu](scripts/download_images.py) na automatizované sťahovanie fotiek chrupu z webovej stránky spoločnosti Invisalign
- [roztriedenie fotiek podľa pohľadu](scripts/split_data_by_view.py) - front, upper, lower, left a right
- predspracovanie fotiek pre účely trénovania siete [pridaním okrajov](scripts/add_padding.py) alebo [orezaním](scripts/center_crop.py) na veľkost 256x256 pixelov
- [skript](scripts/flip_images_horizontally.py) na horizontálne prevrátenie obrázkov 
- použitá [implementácia DCGAN siete](https://keras.io/examples/generative/dcgan_overriding_train_step/)
- použitá [implementácia PGGAN siete](https://github.com/akanimax/pro_gan_pytorch)
- použitá [implementácia StyleGAN siete](https://github.com/NVlabs/stylegan3)
- použitá [implementácia GANformer siete](https://github.com/dorarad/gansformer/tree/main/pytorch_version)


## Výsledky
- ukážky vygenerovaných obrázkov použitím sietí DCGAN, PGGAN, StyleGAN a GANformer sú zobrazené v priečinku [images](images)
- skripty na vytvorenie grafov a výsledné grafy z evaluácie výsledkov sa nachádzajú v priečinku [evaluation](evaluation)