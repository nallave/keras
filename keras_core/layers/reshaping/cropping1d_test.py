import numpy as np
import pytest

from keras_core import backend
from keras_core import layers
from keras_core import operations as ops
from keras_core import testing


class CroppingTest(testing.TestCase):
    def test_cropping_1d(self):
        inputs = np.random.rand(3, 5, 7)

        # Cropping with different values on the left and the right.
        self.run_layer_test(
            layers.Cropping1D,
            init_kwargs={"cropping": (1, 2)},
            input_data=inputs,
            expected_output=ops.convert_to_tensor(inputs[:, 1:3, :]),
        )
        # Same cropping on the left and the right.
        self.run_layer_test(
            layers.Cropping1D,
            init_kwargs={"cropping": (1, 1)},
            input_data=inputs,
            expected_output=ops.convert_to_tensor(inputs[:, 1:4, :]),
        )
        # Same cropping on the left and the right provided as an int.
        self.run_layer_test(
            layers.Cropping1D,
            init_kwargs={"cropping": 1},
            input_data=inputs,
            expected_output=ops.convert_to_tensor(inputs[:, 1:4, :]),
        )
        # Cropping on the right only.
        self.run_layer_test(
            layers.Cropping1D,
            init_kwargs={"cropping": (0, 1)},
            input_data=inputs,
            expected_output=ops.convert_to_tensor(inputs[:, 0:4, :]),
        )
        # Cropping on the left only.
        self.run_layer_test(
            layers.Cropping1D,
            init_kwargs={"cropping": (1, 0)},
            input_data=inputs,
            expected_output=ops.convert_to_tensor(inputs[:, 1:5, :]),
        )

    @pytest.mark.skipif(
        not backend.DYNAMIC_SHAPES_OK,
        reason="Backend does not support dynamic shapes",
    )
    def test_cropping_1d_with_dynamic_batch_size(self):
        input_layer = layers.Input(batch_shape=(None, 5, 7))
        permuted = layers.Cropping1D((1, 2))(input_layer)
        self.assertEqual(permuted.shape, (None, 2, 7))

    def test_cropping_1d_errors_if_cropping_more_than_available(self):
        with self.assertRaises(ValueError):
            input_layer = layers.Input(shape=(3, 4, 7))
            layers.Cropping1D(cropping=(2, 3))(input_layer)