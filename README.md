# urdu-synth
Synthetic text generation for Urdu Text Recognition

# Command
* Create dataset using the following command
```python3 run.py --language ur --count 1000 --length 10 --max_length 100 --random --name_format 2 --height 128 --thread_count 8 --skew_angle 10 --random_skew --blur 2 --random_blur --salt_and_pepper 0.1 --distorsion 3 --distorsion_orientation 2 --background 3 --random_fit --random_resize --random_crop --random_shearx --random_margins --margins 5,5,5,5 --output_dir 1k_images ```

* Run ```python3 run.py --help``` for help

# Reference
1. [trdg library](https://github.com/Belval/TextRecognitionDataGenerator)