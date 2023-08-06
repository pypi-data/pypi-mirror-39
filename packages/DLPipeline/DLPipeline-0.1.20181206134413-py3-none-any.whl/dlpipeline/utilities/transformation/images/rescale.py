import skimage.transform


def transform_images(images: list, size: tuple = (224, 224), mode: str = 'constant') -> list:
  '''

  :param mode:
  :param size:
  :rtype: list
  :param images: list
  :return: list
  '''
  new_images = []

  for image in images:
    new_image = skimage.transform.resize(image, size, mode=mode)
    new_images.append(new_image)

  return new_images
