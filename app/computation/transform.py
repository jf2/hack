import ee


def z_score(img: ee.Image):
    t_mean = img.reduce(ee.Reducer.mean())
    t_mean_mean = t_mean.reduce(ee.Reducer.mean())
    t_mean_std = t_mean.reduce(ee.Reducer.stdDev())

    return (t_mean.subtract(t_mean_mean)).divide(t_mean_std)


def mean(img: ee.Image):
    return img.reduce(ee.Reducer.mean())


def unit(img: ee.Image, epsilon: ee.Image):
    t_max = img.reduce(ee.Reducer.max())
    t_min = img.reduce(ee.Reducer.min())

    united = img.subtract(t_min).divide((t_max.subtract(t_min)).add(epsilon))

    return united