# coding:utf-8
import dict_ext


def may_update_by_dict(row, row_dict: dict):
    should_update = False

    for key, value in row_dict.items():
        if getattr(row, key) != value:
            setattr(row, key, value)
            should_update = True

    if should_update:
        row.save()

    return row


def may_update(row, source, keys):
    """
    On-demand Save

    :param row:     orm row
    :param source:  source dict/object
    :param keys:    keys/attributes
    :return:        orm row
    """
    row_dict = dict_ext.get_dict_by_keys(
        source=source,
        keys=keys,
    )

    return may_update_by_dict(row, row_dict)


def get_or_create_may_update(orm_model, source, keys, defaults: dict = None, **kwargs):
    """
    Get_or_create, may update

    :param orm_model:   orm model
    :param source:      source dict/object
    :param keys:        keys/attributes
    :param defaults:    default dict
    :param kwargs:      **kwargs
    :return:            orm row, created
    """
    row_dict = dict_ext.get_dict_by_keys(
        source=source,
        keys=keys,
    )

    defaults = defaults or dict()

    row, created = orm_model.objects.get_or_create(defaults=dict(row_dict, **defaults), **kwargs)

    if created:
        return row

    return may_update_by_dict(row, row_dict)
