#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Submission controllers for the band structure calculation pipeline."""

from aiida import orm
from aiida_quantumespresso.workflows.pw.relax import PwRelaxWorkChain
from aiida_quantumespresso.workflows.pw.bands import PwBandsWorkChain

from aiida_submission_controller import FromGroupSubmissionController


class PwRelaxSubmissionController(FromGroupSubmissionController):
    """SubmissionController to run PwRelaxWorkChains from a group of `StructureData` nodes."""

    pw_code: str
    """The label of the `Code` to use for the `PwRelaxWorkChain`."""
    overrides: dict = {}
    """A dictionary of overrides to pass to `PwRelaxWorkChain.get_builder_from_protocol()`."""

    def get_inputs_and_processclass_from_extras(self, extras_values):
        parent_node = self.get_parent_node_from_extras(extras_values)

        builder = PwRelaxWorkChain.get_builder_from_protocol(
            code=orm.load_code(self.pw_code),
            structure=parent_node,
            overrides=self.overrides,
            protocol='fast'
        )
        return builder


class PwBandsSubmissionController(FromGroupSubmissionController):
    """SubmissionController to run PwBandsWorkChains from a group of parent nodes."""

    pw_code: str
    """The label of the `Code` to use for the `PwBandsWorkChain`."""
    overrides: dict = {}
    """A dictionary of overrides to pass to `PwBandsWorkChain.get_builder_from_protocol()`."""

    def get_inputs_and_processclass_from_extras(self, extras_values):
        parent_node = self.get_parent_node_from_extras(extras_values)

        structure = parent_node.outputs.output_structure

        builder = PwBandsWorkChain.get_builder_from_protocol(
            code=orm.load_code(self.pw_code),
            structure=structure,
            overrides=self.overrides,
            protocol='fast'
        )
        builder.pop('relax')

        return builder
