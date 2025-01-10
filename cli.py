#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface for the example High-Throughput project."""

import time

from ase.build import bulk

from aiida import orm, load_profile
from controllers import PwRelaxSubmissionController, PwBandsSubmissionController
import typer

load_profile()

app = typer.Typer()


@app.command()
def init():

    _, _ = orm.Group.collection.get_or_create('workchain/relax')
    _, _ = orm.Group.collection.get_or_create('workchain/bands')

    structure_group, created = orm.Group.collection.get_or_create('structures')

    if created:
        for element in ("Al", "Cu", "Fe", "Ni", "Au"):
            structure = orm.StructureData(ase=bulk(element, a=4.2, cubic=True))
            structure.store()
            structure_group.add_nodes(structure)


@app.command()
def run():

    while True:

        relax_controller = PwRelaxSubmissionController(
            group_label='workchain/relax',
            parent_group_label='structures',
            pw_code='pw@localhost',
            max_concurrent=2,
        )

        relax_controller.submit_new_batch(verbose=True)

        bands_controller = PwBandsSubmissionController(
            group_label='workchain/bands',
            parent_group_label='workchain/relax',
            pw_code='pw@localhost',
            max_concurrent=1,
            filters={"attributes.exit_status": 0},
        )

        bands_controller.submit_new_batch(verbose=True)

        time.sleep(30)


if __name__ == "__main__":
    app()
