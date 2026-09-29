import unittest
from unittest.mock import patch

import Labs.LEC08_Animation.animation_viewer as animation_viewer

from Labs.LEC08_Animation.animation_viewer import (
    ANIMATION_FRAMES,
    ANIMATION_ORDER,
    MIN_DISPLAY_HEIGHT,
    REPEAT_LIMIT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    AnimationSequence,
    get_frame_destination_size,
    get_frame_source_rect,
)


class AnimationViewerTests(unittest.TestCase):
    def test_frame_metadata_and_display_bounds(self):
        frames = [frame for sequence in ANIMATION_FRAMES.values() for frame in sequence]
        self.assertEqual({name: len(frames) for name, frames in ANIMATION_FRAMES.items()}, {
            "A": 8,
            "B": 4,
            "C": 6,
            "D": 5,
        })
        self.assertEqual(len(frames), 23)

        for frame in frames:
            source_x, source_y, source_width, source_height = get_frame_source_rect(frame)
            self.assertGreaterEqual(source_x, 0)
            self.assertGreaterEqual(source_y, 0)
            self.assertGreater(source_width, 0)
            self.assertGreater(source_height, 0)
            draw_width, draw_height = get_frame_destination_size(frame)
            self.assertGreaterEqual(draw_height, SCREEN_HEIGHT / 2)
            self.assertLessEqual(draw_width, SCREEN_WIDTH)
            self.assertAlmostEqual(
                draw_width / draw_height,
                source_width / source_height,
                delta=0.002,
            )
        self.assertEqual(MIN_DISPLAY_HEIGHT, SCREEN_HEIGHT // 2)

    def test_all_animations_repeat_pause_and_wrap(self):
        sequence = AnimationSequence()
        observed_frames = {name: set() for name in ANIMATION_ORDER}
        transitions = []
        completed_cycles = []
        previous_name = None
        previous_pause = None

        for step in range(311):
            current_time = step * 0.05
            name, frame = sequence.update(current_time)
            observed_frames[name].add(frame)
            if name != previous_name:
                transitions.append((name, current_time))
                previous_name = name
            if previous_pause is None and sequence.pause_started_at is not None:
                completed_cycles.append((name, sequence.repeat_count))
            previous_pause = sequence.pause_started_at

        self.assertEqual([name for name, _ in transitions], ["A", "B", "C", "D", "A"])
        for (name, transition_time), expected_time in zip(
            transitions[1:], (5.0, 8.0, 12.0, 15.5)
        ):
            self.assertAlmostEqual(transition_time, expected_time, delta=0.05)
        self.assertEqual(completed_cycles, [(name, REPEAT_LIMIT) for name in ANIMATION_ORDER])
        for name in ANIMATION_ORDER:
            self.assertEqual(observed_frames[name], set(ANIMATION_FRAMES[name]))

    def test_invalid_sequence_is_rejected(self):
        with self.assertRaises(ValueError):
            AnimationSequence(animation_frames={}, animation_order=())
        with self.assertRaises(ValueError):
            AnimationSequence(animation_frames={"A": ()}, animation_order=("A",))

    def test_clock_rollback_and_nonfinite_time(self):
        sequence = AnimationSequence()
        with self.assertRaises(ValueError):
            sequence.update(float("nan"))

        name, frame = sequence.update(1.0)
        self.assertEqual((name, frame), ("A", ANIMATION_FRAMES["A"][0]))
        name, frame = sequence.update(0.5)
        self.assertEqual((name, frame), ("A", ANIMATION_FRAMES["A"][0]))
        name, frame = sequence.update(0.6)
        self.assertEqual((name, frame), ("A", ANIMATION_FRAMES["A"][1]))

    def test_run_closes_canvas_when_rendering_fails(self):
        with (
            patch.object(animation_viewer, "open_canvas"),
            patch.object(animation_viewer, "close_canvas") as close_canvas,
            patch.object(animation_viewer, "clear_canvas"),
            patch.object(animation_viewer, "update_canvas"),
            patch.object(animation_viewer, "load_image", return_value=object()),
            patch.object(animation_viewer, "get_time", return_value=0.0),
            patch.object(animation_viewer, "draw_frame", side_effect=RuntimeError("draw failed")),
        ):
            with self.assertRaisesRegex(RuntimeError, "draw failed"):
                animation_viewer.run()
        close_canvas.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
