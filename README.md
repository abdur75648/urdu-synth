# Urdu Synth
High-quality synthetic text data generation for Urdu Text Recognition

**Released as a supplement of [UTRNet: High-Resolution Urdu Text Recognition](https://github.com/abdur75648/UTRNet-High-Resolution-Urdu-Text-Recognition)**

[![UTRNet](https://img.shields.io/badge/UTRNet:%20High--Resolution%20Urdu%20Text%20Recognition-blueviolet?logo=github&style=flat-square)](https://github.com/abdur75648/UTRNet-High-Resolution-Urdu-Text-Recognition)
[![Website](https://img.shields.io/badge/Website-Visit%20Here-brightgreen?style=flat-square)](https://abdur75648.github.io/UTRNet/)
[![arXiv](https://img.shields.io/badge/arXiv-2306.15782-darkred.svg)](https://arxiv.org/abs/2306.15782)

## Steps to run the code
* Create dataset using the following command
```python3 run.py --count 1000 --length 10 --max_length 100 --random --name_format 2 --height 128 --thread_count 8 --skew_angle 10 --random_skew --blur 2 --random_blur --salt_and_pepper 0.1 --distorsion 3 --distorsion_orientation 2 --background 3 --random_fit --random_resize --random_crop --random_shearx --random_margins --margins 5,5,5,5 --output_dir 1k_images ```

* Run ```python3 run.py --help``` for help

## Useful Links
1. Download the [UTRSet-Synth](https://csciitd-my.sharepoint.com/:u:/g/personal/ch7190150_iitd_ac_in/EUVd7N9q5ZhDqIXrcN_BhMkBKQuc00ivNZ2_jXZArC2f0g?e=Gubr7c) dataset
2. For more information & other resources, visit [Project Webpage](https://abdur75648.github.io/UTRNet/)
3. Main codebase - [UTRNet Repo](https://github.com/abdur75648/UTRNet-High-Resolution-Urdu-Text-Recognition)

## Note
1. Based on the [trdg library](https://github.com/Belval/TextRecognitionDataGenerator)
2. The code (& the generated dataset) is for research purposes only and must not be used for any other purpose without the author's explicit permission.

## Citation
If you use the code/model/dataset, please cite the following paper:

```BibTeX
@article{rahman2023utrnet,
      title={UTRNet: High-Resolution Urdu Text Recognition In Printed Documents}, 
      author={Abdur Rahman and Arjun Ghosh and Chetan Arora},
      journal={arXiv preprint arXiv:2306.15782},
      year={2023},
      eprint={2306.15782},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      doi = {https://doi.org/10.48550/arXiv.2306.15782},
      url = {https://arxiv.org/abs/2306.15782}
}
```

### License
[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/). This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/) for Noncommercial (academic & research) purposes only and must not be used for any other purpose without the author's explicit permission.
