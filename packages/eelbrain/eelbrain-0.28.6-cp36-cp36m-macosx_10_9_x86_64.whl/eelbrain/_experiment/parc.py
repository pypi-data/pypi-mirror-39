import re

from .definitions import DefinitionError, Definition


COMBINATION_PARC = 'combination'
FS_PARC = 'subject_parc'  # Parcellation that come with every MRI-subject
FSA_PARC = 'fsaverage_parc'  # Parcellation that comes with fsaverage
SEEDED_PARC = 'seeded'
INDIVIDUAL_SEEDED_PARC = 'individual seeded'
SEEDED_PARC_RE = re.compile('^(.+)-(\d+)$')


class Parcellation(Definition):
    DICT_ATTRS = ('kind',)
    make = False
    morph_from_fsaverage = False

    def __init__(self, name, views=None):
        self.name = name
        self.views = views


class CombinationParcellation(Parcellation):
    "Recombine labels from an existing parcellation"
    DICT_ATTRS = ('kind', 'base', 'labels')
    kind = COMBINATION_PARC
    make = True

    def __init__(self, name, base, labels, views=None):
        Parcellation.__init__(self, name, views)
        self.base = base
        self.labels = labels


class EelbrainParcellation(Parcellation):
    "Parcellation that has special make rule"
    kind = 'eelbrain_parc'
    make = True

    def __init__(self, name, morph_from_fsaverage, views=None):
        Parcellation.__init__(self, name, views)
        self.morph_from_fsaverage = morph_from_fsaverage


class FreeSurferParcellation(Parcellation):
    "Parcellation that comes with FreeSurfer"
    kind = FS_PARC


class FSAverageParcellation(Parcellation):
    "Parcellation that comes with FSAverage"
    kind = FSA_PARC
    morph_from_fsaverage = True


class LabelParcellation(Parcellation):
    "Assemble parcellation from labels"
    DICT_ATTRS = ('kind', 'labels')
    kind = 'label_parc'
    make = True

    def __init__(self, name, labels, views=None):
        Parcellation.__init__(self, name, views)
        self.labels = labels if isinstance(labels, tuple) else tuple(labels)


class SeededParcellation(Parcellation):
    "Parcellation that is grown from seed vertices"
    DICT_ATTRS = ('kind', 'seeds', 'surface', 'mask')
    kind = SEEDED_PARC
    make = True

    def __init__(self, name, seeds, mask=None, surface='white', views=None):
        Parcellation.__init__(self, name, views)
        self.seeds = seeds
        self.mask = mask
        self.surface = surface

    def seeds_for_subject(self, subject):
        return self.seeds


class IndividualSeededParcellation(SeededParcellation):
    "Seed parcellation with individual seeds for each subject"
    kind = INDIVIDUAL_SEEDED_PARC
    morph_from_fsaverage = False

    def __init__(self, name, seeds, mask=None, surface='white', views=None):
        SeededParcellation.__init__(self, name, seeds, mask, surface, views)
        labels = tuple(self.seeds)
        label_subjects = {label: sorted(self.seeds[label].keys()) for label in labels}
        subjects = label_subjects[labels[0]]
        if not all(label_subjects[label] == subjects for label in labels[1:]):
            raise DefinitionError(
                "parc %s: Some labels are missing subjects. if a subject does not "
                "have a label, use an empty tuple as seed, e.g.: 'R0001': ()" % self.name)
        self.subjects = subjects

    def seeds_for_subject(self, subject):
        if subject not in self.subjects:
            raise DefinitionError("Parc %s not defined for subject %s" % (self.name, subject))
        seeds = {name: self.seeds[name][subject] for name in self.seeds}
        # filter out missing
        return {name: seed for name, seed in seeds.items() if seed}


PARC_CLASSES = {
    COMBINATION_PARC: CombinationParcellation,
    FS_PARC: FreeSurferParcellation,
    FSA_PARC: FSAverageParcellation,
    SEEDED_PARC: SeededParcellation,
    INDIVIDUAL_SEEDED_PARC: IndividualSeededParcellation,
}
