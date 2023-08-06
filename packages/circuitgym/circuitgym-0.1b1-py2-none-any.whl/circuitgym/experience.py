import pandas as pd
import numpy as np
import os.path


def _write_experience_file(datablock, directory, filename, datablock_columns, ncircuits, use_multiindex=False):
    filepath = os.path.join(directory, filename)
    os.makedirs(directory, exist_ok=True)
    datablock = np.vstack(datablock).T
    if use_multiindex:
        raise NotImplementedError
        # subcolumns = []
        # for i, name in enumerate(datablock_columns):
        #     for j in range(np.max([row[i].size for row in datablock])):
        #         subcolumns.append((name, name + '_' + str(j)))
        # mi = pd.MultiIndex.from_tuples(subcolumns)
        #
        # for i, row in enumerate(datablock):
        #     datablock[i] = np.hstack(row)
        #
        # table = pd.DataFrame(datablock, columns=mi)
        #
        # with pd.HDFStore(filepath) as store:
        #     store['table'] = table
        #     store['ncircuits'] = pd.DataFrame(np.array([3],dtype=int))

    else:
        shapes={}
        with pd.HDFStore(filepath, mode='w') as store:
            for i, name in enumerate(datablock_columns):
                shapes.update({name: datablock[i][0].shape})
                store[name] = pd.DataFrame(np.stack(datablock[i], axis=0).reshape(len(datablock[i]),-1))
            store['ncircuits'] = pd.DataFrame(np.array([[ncircuits]]))
            store['shapes'] = pd.DataFrame.from_dict(shapes, orient='index')


def _is_single_table(store):
    size = len(store.keys())
    return True if size == 1 else False

def get_record_length(filename):
    with pd.HDFStore(filename, mode='r') as store:
        if _is_single_table(store):
            return store['table'].shape[0]
        else:
            return store['action'].shape[0]

def read_experience_file(filename, column_names=None, rows=None):
    data = {}
    with pd.HDFStore(filename, mode='r') as store:
        if _is_single_table(store):
            if not rows:
                rows = np.arange(0,store['table'].shape[0])
            if not column_names:
                column_names = store['table'].columns()

            for itemname in column_names:
                data.update({itemname: np.array(
                    [np.hsplit(entry[1].values, 2) if not entry[1].values.size % 2 \
                         else entry[1].values for entry in store['table'][itemname].iterrows()]
                ).squeeze()[rows]
                             })
        else:
            if not column_names:
                column_names = [key.lstrip('/') for key in store.keys()]
            for itemname in column_names:
                data.update({itemname: store[itemname].values if not rows else store[itemname].values[rows]})
            if not np.isscalar(store['ncircuits']):
                data.update({'ncircuits': store['ncircuits'].values[0][0]})
            else:
                data.update({'ncircuits': store['ncircuits']})
            data.update({'shapes': store['shapes']})

    return data


def construct_aug_inputs(state, action):
    return np.hstack((
        np.expand_dims(state, axis=1),
        action
    ))


def get_circuit_split(store, column_name, circuit_no):
    if isinstance(store, pd.HDFStore):
        data = store[column_name].values
    else:
        data = store[column_name]
    if np.isscalar(store['ncircuits']):
        return np.split(data, store['ncircuits'], axis=1)[circuit_no]
    else:
        return np.split(data, store['ncircuits'].values[0,0], axis=1)[circuit_no]

def update_augmentor_targets(filenames, augmentor, aug_ckt_ind):
    for file in filenames:
        with pd.HDFStore(file, mode='r+') as store:
            augsig = augmentor(
                get_circuit_split(store, 'state', aug_ckt_ind),
                get_circuit_split(store, 'action', aug_ckt_ind)
            )
            overlay = np.split(np.zeros(store['response'].shape), store['ncircuits'].values[0,0], axis=1)
            overlay[aug_ckt_ind] += augsig
            overlay = np.hstack(overlay)
            store['response'] += overlay


def get_diff_output_mse(filename, nsamples=None):
    data = read_experience_file(filename)
    rows = np.random.random_integers(0, data['state'].shape[0] - 1, int(nsamples)) \
        if nsamples else np.arange(0, data['state'].shape[0])
    err = get_circuit_split(data, 'response', 0)[rows] - get_circuit_split(data, 'response', 1)[rows]

    return np.mean(err**2, axis=1)


def get_base_output(filename, nsamples=None):
    data = read_experience_file(filename)
    rows = np.random.random_integers(0, data['state'].shape[0] - 1, int(nsamples)) \
        if nsamples else np.arange(0, data['state'].shape[0])

    return get_circuit_split(data, 'response', 0)[rows]


def get_rewards(filename, nsamples=None):
    data = read_experience_file(filename)
    rows = np.random.random_integers(0, data['state'].shape[0] - 1, int(nsamples)) \
        if nsamples else np.arange(0, data['state'].shape[0])

    return data['reward'][rows]


def get_aug_output(filename, nsamples=None):
    data = read_experience_file(filename)
    rows = np.random.random_integers(0, data['state'].shape[0] - 1, int(nsamples)) \
        if nsamples else np.arange(0, data['state'].shape[0])

    return get_circuit_split(data,'response',1)[rows]

def get_augmentor_targets(filename, aug_ckt_ind=1, nsamples=None):
    data = read_experience_file(filename, ['state', 'action', 'response'])
    rows = np.random.random_integers(0, data['state'].shape[0] - 1, int(nsamples)) if nsamples else \
        range(data['state'].shape[0])

    x = construct_aug_inputs(
        get_circuit_split(data, 'state', aug_ckt_ind)[rows].squeeze(),
        get_circuit_split(data, 'action', aug_ckt_ind)[rows].squeeze()
    )

    y = get_circuit_split(data,'response', 0)[rows] - get_circuit_split(data,'response', 1)[rows]

    return x, y


def fake():
    return True
