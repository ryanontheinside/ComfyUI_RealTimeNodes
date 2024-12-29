from .detectors import MotionDetector, BrightnessDetector
from ..base.control_base import ControlNodeBase
from ..base.detector_base import ROIAction
from enum import Enum
import numpy as np

class RegionOfInterest(ControlNodeBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "detector": ("DETECTOR",),  # Takes configured detector node output
                "action": (list(action.value for action in ROIAction),),
                "value": ("FLOAT", {"default": 0.1, "step": 0.01}),
            },
            "optional": {
                "next_roi": ("ROI",)
            }
        }

    RETURN_TYPES = ("ROI",)
    FUNCTION = "update"
    CATEGORY = "real-time/control/detection"

    def update(self, mask, detector, action, value, next_roi=None):
        """Implements required update method from ControlNodeBase"""
        mask_np = mask[0].cpu().numpy()
        
        # Calculate bounds
        coords = np.nonzero(mask_np)
        bounds = (
            coords[0].min() if len(coords[0]) > 0 else 0,
            coords[1].min() if len(coords[0]) > 0 else 0,
            coords[0].max() if len(coords[0]) > 0 else 0,
            coords[1].max() if len(coords[0]) > 0 else 0
        )
        
        return ({
            "mask": mask_np,
            "bounds": bounds,
            "detector": detector,  # Now takes pre-configured detector
            "action": action,
            "value": value,
            "next": next_roi
        },)

class MotionDetectorNode(ControlNodeBase):
    """Configures a motion detector with specific settings"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "threshold": ("FLOAT", {
                    "default": 0.1, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.01,
                    "tooltip": "Motion detection sensitivity"
                }),
                "blur_size": ("INT", {
                    "default": 5, 
                    "min": 1, 
                    "max": 21, 
                    "step": 2,
                    "tooltip": "Size of blur kernel for noise reduction"
                })
            }
        }

    RETURN_TYPES = ("DETECTOR",)
    FUNCTION = "update"
    CATEGORY = "real-time/control/detection"

    def update(self, threshold, blur_size):
        """Implements required update method from ControlNodeBase"""
        detector = MotionDetector()
        detector.setup(threshold=threshold, blur_size=blur_size)
        return (detector,) 


class BrightnessDetectorNode(ControlNodeBase):
    """Configures a brightness detector with specific settings"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "threshold": ("FLOAT", {
                    "default": 0.5, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.01,
                    "tooltip": "Brightness threshold for visualization"
                }),
                "use_average": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Use average brightness instead of maximum"
                })
            }
        }

    RETURN_TYPES = ("DETECTOR",)
    FUNCTION = "update"
    CATEGORY = "real-time/control/detection"

    def update(self, threshold, use_average):
        """Implements required update method from ControlNodeBase"""
        detector = BrightnessDetector()
        detector.setup(threshold=threshold, use_average=use_average)
        return (detector,)