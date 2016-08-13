from unittest import TestCase
from unittest.mock import patch, call
from engine.scenes import BaseScene
from engine.controllers import SceneController


class TestSceneA(BaseScene):
    def __init__(self, controller):
        super().__init__(controller, 'TestSceneA')


class TestSceneB(BaseScene):
    def __init__(self, controller):
        super().__init__(controller, 'TestSceneB')


@patch.object(BaseScene, 'show')
@patch.object(BaseScene, 'cleanup')
class SceneControllerTest(TestCase):
    """Tests for the SceneController class"""

    """SceneController.__init__"""
    def test_new_scene_controller_presents_initial(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        self.assertEqual(scene_controller.scene_stack[-1], TestSceneA)

    """SceneController.top"""
    def test_initial_is_at_top_of_stack(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        self.assertEqual(scene_controller.top, TestSceneA)

    def test_additional_scene_pushed_on_stack_is_at_top(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.push(TestSceneB)
        self.assertEqual(scene_controller.top, TestSceneB)

    """SceneController.push"""
    def test_pushing_scenes_results_in_taller_stack(self, cleanup_mock, show_mock):
        scene_controller = SceneController()
        self.assertEqual(len(scene_controller.scene_stack), 0)
        scene_controller.push(TestSceneA)
        self.assertEqual(len(scene_controller.scene_stack), 1)

    @patch.object(TestSceneA, 'show')
    def test_new_scene_is_displayed(self, scene_mock, cleanup_mock, show_mock):
        scene_controller = SceneController()
        scene_controller.push(TestSceneA)
        scene_mock.assert_called_once_with()

    @patch.object(TestSceneB, 'cleanup')
    def test_old_scene_is_cleaned_up(self, scene_mock, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneB)
        scene_controller.push(TestSceneA)
        scene_mock.assert_called_once_with()

    def test_new_scene_instantiated_to_current_scene(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.push(TestSceneB)
        self.assertEqual(scene_controller.current_scene.__class__, TestSceneB)

    """SceneController.pop"""
    def test_pushing_scenes_results_in_shorter_stack(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.push(TestSceneA)
        self.assertEqual(len(scene_controller.scene_stack), 2)
        scene_controller.pop()
        self.assertEqual(len(scene_controller.scene_stack), 1)

    @patch.object(TestSceneB, 'show')
    def test_scene_below_is_displayed(self, scene_mock, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneB)
        scene_controller.push(TestSceneA)
        scene_controller.pop()
        scene_mock.assert_has_calls((call(), call()))

    def test_top_scene_is_cleaned_up(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.push(TestSceneB)
        cleanup_mock.assert_called_once_with()

    def test_old_scene_instantiated_to_current_scene(self, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.push(TestSceneB)
        scene_controller.pop()
        self.assertEqual(scene_controller.current_scene.__class__, TestSceneA)

    @patch.object(SceneController, 'exit')
    def test_emptying_stack_results_in_exit(self, exit_mock, cleanup_mock, show_mock):
        scene_controller = SceneController(initial=TestSceneA)
        scene_controller.pop()
        exit_mock.assert_called_once_with()
