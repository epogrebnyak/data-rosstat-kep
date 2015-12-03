
def demo_with_axes():
    # - для понимания, предположим я закрыл окно в котором были отрисованы графики вызовом ниже
    #   у меня есть z, массив объетов subplot - как я могу снова нарисовать z в отдельной figure?

    df = get_dataframe(get_var_list(), "m", "1999-01")
    df = df.iloc[:,0:6]
    z = many_plots_per_page(df, 3, 2)

    # DN: Закрытие окна ещё не означает, что все ссылки на соответствующий figure уничтожены.
    # Эта функция отвечает за очистку следов figure:
    # https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/_pylab_helpers.py#L50
    # Её же вызывает plt.close(). Она всего лишь убирает ссылки на figure из внутреннего состояния
    # matplotlib, после чего вызывает сборщик мусора. Поскольку ссылки на figure всё ещё остаются
    # (внутри z, через z.figure), figure из памяти не удаляется.

    old_fig_number = z[0, 0].figure.number
    plt.close(old_fig_number)

    # Теперь matplotlib забыл о существовании figure, но объект всё ещё доступен через z.figure.
    # z -- это всего лишь ndarray из Axes:

    import numpy as np
    assert isinstance(z, np.ndarray)
    assert z.shape == (3, 2)

    # Теперь можно создать новый figure и присоединить к нему старые Axes:
    fig = plt.figure("new figure", figsize=A4_SIZE_PORTRAIT)

    for row in z:
        for ax in row:
            assert isinstance(ax, matplotlib.axes.Axes)
            ax.figure = fig
            fig.add_subplot(ax)

    # Появится одно окно с заголовком "new figure"
    plt.show()