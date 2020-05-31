
   #!/bin/bash
   # Basic while loop
   counter=0
   counter_2=1
   while [ $counter -le 500 ]
   do
   echo $counter
   if [ $counter -lt 9 ] ; then
	   ./bin/nicp_depth_image_registration /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_0000$counter.png /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_0000$counter_2.png 1
   elif [ $counter -eq 9 ] ; then
	   ./bin/nicp_depth_image_registration /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_0000$counter.png /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_000$counter_2.png 1
   elif [ $counter -gt 9 ] && [ $counter -lt 99 ] ; then
	   ./bin/nicp_depth_image_registration /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_000$counter.png /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_000$counter_2.png 1
   elif [ $counter -eq 99 ] ; then
	   ./bin/nicp_depth_image_registration /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_000$counter.png /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_00$counter_2.png 1
   else [ $counter -gt 99 ]
	   ./bin/nicp_depth_image_registration /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_00$counter.png /home/filip/Downloads/nicp/nicp_depth_camera_tracking_code/bin/Sequence_2_Kin_2/depth/depth_00$counter_2.png 1
   fi

   ((counter++))
   ((counter_2++))
   done

   python3 do_nicp_odometry.py 

   echo All done
																																																																																																																																																																																																																																			
