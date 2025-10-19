import json
import os
from django.conf import settings
from .models import Truck, TruckEvent, SafetyEvent, Alert, Equipment
import logging

logger = logging.getLogger(__name__)

class DetectionProcessor:
    def __init__(self):
        self.json_dir = settings.JSON_DETECTIONS_DIR
        self.processed_dir = os.path.join(self.json_dir, 'processed')
        
        # Create directories if they don't exist
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def monitor_detection_files(self):
        """Simple file monitoring for Azure"""
        try:
            self.process_new_detections()
        except Exception as e:
            logger.error(f"Error monitoring detection files: {str(e)}")
    
    def process_new_detections(self):
        """Process any new detection files"""
        try:
            for filename in os.listdir(self.json_dir):
                if filename.endswith('.json') and not filename.startswith('processed_'):
                    file_path = os.path.join(self.json_dir, filename)
                    self.process_detection_file(file_path)
        except Exception as e:
            logger.error(f"Error processing detection files: {str(e)}")
    
    def process_detection_file(self, file_path):
        """Process a single detection file"""
        try:
            with open(file_path, 'r') as f:
                detection_data = json.load(f)
            
            logger.info(f"Processing detection file: {file_path}")
            
            # Process different types of detections
            if 'truck_detections' in detection_data:
                self._process_truck_detections(detection_data['truck_detections'])
            
            if 'safety_violations' in detection_data:
                self._process_safety_violations(detection_data['safety_violations'])
            
            # Move processed file to archive
            processed_filename = f"processed_{os.path.basename(file_path)}"
            archive_path = os.path.join(self.processed_dir, processed_filename)
            os.rename(file_path, archive_path)
            
            logger.info(f"Successfully processed: {file_path}")
            
        except Exception as e:
            logger.error(f"Error processing detection file {file_path}: {str(e)}")
    
    def _process_truck_detections(self, detections):
        """Process truck movement and status detections"""
        for detection in detections:
            try:
                truck_id = detection.get('truck_id')
                event_type = detection.get('event_type')
                location = detection.get('location', 'Unknown')
                
                # Get or create truck
                truck, created = Truck.objects.get_or_create(
                    truck_id=truck_id,
                    defaults={
                        'license_plate': detection.get('license_plate', 'UNKNOWN'),
                        'driver_name': detection.get('driver_name', 'Unknown'),
                        'company': detection.get('company', 'Unknown'),
                        'current_status': 'gate_in'
                    }
                )
                
                # Update truck status based on event
                status_map = {
                    'gate_in': 'gate_in',
                    'docked': 'docked', 
                    'loading_start': 'loading',
                    'loading_end': 'loading',
                    'departed': 'departed'
                }
                
                if event_type in status_map:
                    truck.current_status = status_map[event_type]
                    truck.save()
                
                # Create event
                TruckEvent.objects.create(
                    truck=truck,
                    event_type=event_type,
                    location=location,
                    notes=detection.get('notes', 'Automated detection')
                )
                
                logger.info(f"Processed truck event: {truck_id} - {event_type}")
                
            except Exception as e:
                logger.error(f"Error processing truck detection: {str(e)}")
    
    def _process_safety_violations(self, violations):
        """Process safety violation detections"""
        for violation in violations:
            try:
                safety_event = SafetyEvent.objects.create(
                    violation_type=violation.get('violation_type', 'unsafe_operation'),
                    severity=violation.get('severity', 'medium'),
                    location=violation.get('location', 'Unknown'),
                    description=violation.get('description', 'Safety violation detected')
                )
                
                # Create alert for safety violations
                if violation.get('severity') in ['high', 'critical']:
                    Alert.objects.create(
                        alert_type='safety',
                        priority=violation.get('severity', 'medium'),
                        title=f"Safety Violation - {violation.get('violation_type', 'Unknown')}",
                        message=violation.get('description', 'Critical safety violation detected'),
                    )
                
                logger.info(f"Processed safety violation: {safety_event.violation_type}")
                
            except Exception as e:
                logger.error(f"Error processing safety violation: {str(e)}")