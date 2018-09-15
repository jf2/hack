import ee


def z_score(img: ee.Image):
    t_mean = img.reduce(ee.Reducer.mean())
    t_mean_mean = t_mean.reduce(ee.Reducer.mean())
    t_mean_std = t_mean.reduce(ee.Reducer.stdDev())

    return (t_mean.subtract(t_mean_mean)).divide(t_mean_std)