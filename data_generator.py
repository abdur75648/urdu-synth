import os
import random as rnd

from PIL import Image, ImageFilter

import warnings
warnings.filterwarnings("ignore")
import torchvision.transforms.functional as F
from torchvision.transforms import PILToTensor, ToPILImage

import computer_text_generator, background_generator, distorsion_generator

from utils import salt_and_pepper_noise

"""
try:
    import handwritten_text_generator
except ImportError as e:
    pass
"""

class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        text,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        random_shearx,
        salt_and_pepper,
        background_type,
        distorsion_type,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        random_margins,
        random_crop,
        fit,
        random_fit,
        output_mask,
        word_split,
        image_dir,
        stroke_width=0, 
        stroke_fill="#282828",
        image_mode="RGB",
        random_resize = False,
    ):
        image = None
        
        if random_fit:
            fit = rnd.choice([True, False])

        if random_margins:
            margins = [int(rnd.random()*margin) for margin in margins]
        margin_top, margin_left, margin_bottom, margin_right = margins
        horizontal_margin = margin_left + margin_right
        vertical_margin = margin_top + margin_bottom

        ##########################
        # Create picture of text #
        ##########################
        if is_handwritten:
            raise ValueError("Handwritten model is unavailable")
            """
            if orientation == 1:
                raise ValueError("Vertical handwritten text is unavailable")
            image, mask = handwritten_text_generator.generate(text, text_color)
            """
        else:
            image, mask = computer_text_generator.generate(
                text,
                font,
                text_color,
                size,
                orientation,
                space_width,
                character_spacing,
                fit,
                word_split,
                stroke_width, 
                stroke_fill,
            )
        random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

        rotated_img = image.rotate(
            skewing_angle if not random_skew else random_angle, expand=True)

        rotated_mask = mask.rotate(
            skewing_angle if not random_skew else random_angle, expand=True)

        #############################
        # Apply distorsion to image #
        #############################
        if distorsion_type == 0:
            distorted_img = rotated_img  # Mind = blown
            distorted_mask = rotated_mask
        elif distorsion_type == 1:
            distorted_img, distorted_mask = distorsion_generator.sin(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        elif distorsion_type == 2:
            distorted_img, distorted_mask = distorsion_generator.cos(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )
        else:
            distorted_img, distorted_mask = distorsion_generator.random(
                rotated_img,
                rotated_mask,
                vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
            )

        ##################################
        # Resize image to desired format #
        ##################################

        # Horizontal text
        if orientation == 0:
            new_width = int(
                distorted_img.size[0]
                * (float(size - vertical_margin) / float(distorted_img.size[1]))
            )
            resized_img = distorted_img.resize(
                (new_width, size - vertical_margin), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize((new_width, size - vertical_margin), Image.NEAREST)
            background_width = width if width > 0 else new_width + horizontal_margin
            background_height = size
        # Vertical text
        elif orientation == 1:
            new_height = int(
                float(distorted_img.size[1])
                * (float(size - horizontal_margin) / float(distorted_img.size[0]))
            )
            resized_img = distorted_img.resize(
                (size - horizontal_margin, new_height), Image.ANTIALIAS
            )
            resized_mask = distorted_mask.resize(
                (size - horizontal_margin, new_height), Image.NEAREST
            )
            background_width = size
            background_height = new_height + vertical_margin
        else:
            raise ValueError("Invalid orientation")

        #############################
        # Generate background image #
        #############################
        
        if alignment == 3 and not fit:
            # randomly increase background_width within 0% to 300% of original width # For digits
            background_width = int(background_width * rnd.uniform(1.0, 3.0))
        
        if background_type==4:
            background_type = rnd.choice([0,0,1,3,3,3,3,3,3,3])
        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_dir
            )
        background_mask = Image.new(
            "RGB", (background_width, background_height), (0, 0, 0)
        )

        #############################
        # Place text with alignment #
        #############################

        new_text_width, _ = resized_img.size
        
        alignment = rnd.choice([0, 1, 2]) if alignment == 3 else alignment
        if alignment == 0: #or width == -1:
            background_img.paste(resized_img, (margin_left, margin_top), resized_img)
            background_mask.paste(resized_mask, (margin_left, margin_top))
        elif alignment == 1:
            background_img.paste(
                resized_img,
                (int(background_width / 2 - new_text_width / 2), margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (int(background_width / 2 - new_text_width / 2), margin_top),
            )
        else:
            background_img.paste(
                resized_img,
                (background_width - new_text_width - margin_right, margin_top),
                resized_img,
            )
            background_mask.paste(
                resized_mask,
                (background_width - new_text_width - margin_right, margin_top),
            )

        #######################
        # Apply gaussian blur #
        #######################

        gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        final_image = background_img.filter(gaussian_filter)
        final_mask = background_mask.filter(gaussian_filter)
        
        ############################################
        # Change image mode (RGB, grayscale, etc.) #
        ############################################
        
        if random_crop:
            # randomly crop image within 0% to 7.5% of original height & 0 to 2.5% of original width
            crop_left = int(background_width * rnd.uniform(0.0, 0.025))
            crop_top = int(background_height * rnd.uniform(0.0, 0.075))            
            crop_right = int(background_width * rnd.uniform(0.975, 1.0))
            crop_bottom = int(background_height * rnd.uniform(0.925, 1.0))
            final_image = final_image.crop((crop_left, crop_top, crop_right, crop_bottom))
        
        if random_resize:
            size = final_image.size
            new_size = [rnd.randint(int(0.5*size[0]), int(1.5*size[0])), rnd.randint(int(0.5*size[1]), int(1.5*size[1]))]
            reduce_factor = rnd.random()+1 #rnd.randint(1,3)
            new_size = tuple([int(x/reduce_factor) for x in new_size])
            final_image = final_image.resize(new_size)
            final_mask = final_mask.resize(new_size)
    
        if rnd.random() < salt_and_pepper:
            final_image = salt_and_pepper_noise(final_image)
        
        if random_shearx:
            shearx_factor = rnd.uniform(-0.25,0.5)
            final_image = final_image.transform(final_image.size, Image.Transform.AFFINE, (1, shearx_factor, 0, 0, 1, 0))
        
        """
        if random_transforms:
            final_image = PILToTensor()(final_image)
            final_image = F.adjust_hue(final_image,rnd.random()-0.5)
            final_image = F.adjust_contrast(final_image,rnd.randint(5,15)/10)
            final_image = F.adjust_brightness(final_image,rnd.randint(5,15)/10)
            final_image = F.adjust_saturation(final_image,rnd.randint(5,15)/10)
            final_image = ToPILImage()(final_image)
        """
        
        final_image = final_image.convert(image_mode)
        final_mask = final_mask.convert(image_mode) 

        #####################################
        # Generate name for resulting image #
        #####################################
        # We remove spaces if space_width == 0
        if space_width == 0:
            text = text.replace(" ", "")
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
            mask_name = "{}_{}_mask.png".format(str(index), text)
        elif name_format == 2:
            image_name = "{}.{}".format(str(index), extension)
            mask_name = "{}_mask.png".format(str(index))
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))

        # Save the image
        if out_dir is not None:
            final_image.save(os.path.join(out_dir, image_name))
            if output_mask == 1:
                final_mask.save(os.path.join(out_dir, mask_name))
        else:
            if output_mask == 1:
                return final_image, final_mask
            return final_image
