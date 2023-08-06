def aggregate_array(array, aggr_level, group_lims=None):
    if aggr_level < 1:
        return array
    if group_lims is None:
        group_lims = [list() for k in range(aggr_level)]
        i = -1
    else:
        try:
            i = group_lims[aggr_level - 1][-1]
        except IndexError:
            i = -1
    aggr_array = list()
    if aggr_level == 1:
        for array_elm in array:
            aggr_array.extend(array_elm)
            i += len(array_elm)
            group_lims[0].append(i)
    else:
        for array_elm in array:
            aggr_array.extend(aggregate_array(array=array_elm, aggr_level=aggr_level-1, group_lims=group_lims)[0])
            i += len(array_elm)
            group_lims[aggr_level-1].append(i)
    return aggr_array, group_lims


def group_array(aggr_array, group_lims):
    if len(group_lims) == 1:
        return _group_level(aggr_array, group_lims.pop(0))
    aggr_array = _group_level(aggr_array, group_lims.pop(0))
    return group_array(aggr_array, group_lims)


def _group_level(aggr_array, level_lims):
    grouped_array = [list()]
    for i in range(len(aggr_array)):
        grouped_array[-1].append(aggr_array[i])
        if i == level_lims[0]:
            level_lims.pop(0)
            grouped_array.append(list())
    return list(filter(None, grouped_array))
