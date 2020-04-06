
gabbicompare is a gabbi ContentHander that subclasses the core
JSON handler to provide a way to compare the JSON response from
a known "good" source with a target, where the target is a new
implementation of the same service. Source and target are
assumed to be "live", in the sense that they use the same source
of real data.

See `gabbicompare/tests/gabbits/prove.yaml` for examples.
