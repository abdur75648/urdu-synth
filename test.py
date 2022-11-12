from PIL import Image
img = Image.open("test.jpg")
img_transformed = img.transform(img.size, Image.Transform.AFFINE, (1, -0.9, 0, 0, 1, 0))
img_transformed.save("test_0.9.jpg")
img_transformed = img.transform(img.size, Image.Transform.AFFINE, (1, -0.5, 0, 0, 1, 0))
img_transformed.save("test_0.5.jpg")
img_transformed = img.transform(img.size, Image.Transform.AFFINE, (1, 0.0, 0, 0, 1, 0))
img_transformed.save("test_0.0.jpg")

## 0.5 is best