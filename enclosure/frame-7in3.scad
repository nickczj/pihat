// Phase 4 placeholder: rough envelope only, not printable enclosure geometry.

pcb_width = 174;
pcb_height = 123;
frame_width = 180;
frame_height = 130;
wall = 3;

module pcb_envelope() {
    color("seagreen")
        translate([(frame_width - pcb_width) / 2, (frame_height - pcb_height) / 2, 0])
            cube([pcb_width, pcb_height, 1.6]);
}

module frame_envelope() {
    difference() {
        cube([frame_width, frame_height, wall]);
        translate([wall, wall, -0.1])
            cube([frame_width - 2 * wall, frame_height - 2 * wall, wall + 0.2]);
    }
}

frame_envelope();
translate([0, 0, wall + 1])
    pcb_envelope();

