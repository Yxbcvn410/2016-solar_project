from space import Space


def get_stats(space: Space):
    full_stats = {}
    snapshots = set()
    for body in space.bodies:
        snapshots.update(set([snapshot[0] for snapshot in body.trace]))
    snapshots = list(snapshots)
    snapshots.sort()
    for snapshot_time in snapshots:
        full_snapshot = {}
        for body in space.bodies:
            if snapshot_time in [snapshot[0] for snapshot in body.trace]:
                full_snapshot.update({space.bodies.index(body): body.trace[1:]})
            else:
                full_snapshot.update({space.bodies.index(body):
                                          full_stats[snapshots[snapshots.index(snapshot_time) - 1]][
                                              space.bodies.index(body)]})
        full_stats.update({snapshot_time: full_snapshot})
    return full_stats


def write_stats(stats, filename):
    writer = open(filename, 'w')
    for snapshot in stats:
        writer.write(snapshot + '\t')
        for body in stats[snapshot]:
            writer.write('{}\t{}\t{}\t{}\t'.format(*stats[snapshot][body]))
        writer.write('\n')
    writer.close()


def get_time_axis(stats):
    return list(stats)


def get_dist_axis(stats, body_1, body_2):
    return list(((stats[snapshot][body_1][1] - stats[snapshot][body_2][1]) ** 2 + (
            stats[snapshot][body_1][2] - stats[snapshot][body_2][2]) ** 2) ** 0.5 for snapshot in stats)


def get_vel_axis(stats, body):
    return list((stats[snapshot][body][3] ** 2 + stats[snapshot][body][4] ** 2) ** 0.5 for snapshot in stats)
