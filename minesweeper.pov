///////////////////////////////////////////////////////////
// Persistence of Vision Ray Tracer Scene Description File
// File: minesweeper.inc
// Vers: 3.6
// Desc: Scene file for solving minesweeper
// Date: May 22, 2006
// Auth: David Curtis

#version 3.7;

///////////////////////////////////////////////////////////
// Window Sizes
// +w144 +h144 +iminesweeper.pov
// +w256 +h256 +iminesweeper.pov
// +w480 +h480 +iminesweeper.pov
// +w480 +h256 +iminesweeper.pov
// +w960 +h512 +iminesweeper.pov +o"frames\\minesweeper" +kfi1 +kff100
// +w480 +h256 +iminesweeper.pov +ki1 +kf480 +kfi1 +kff480
// +w1280 +h720 +iminesweeper.pov +P

///////////////////////////////////////////////////////////
// controls
// winners - 1001/61

#declare grid_num = 123567; // possible winner!!!
// #declare grid_num = 125678;
//#declare grid_num = 312568;
//#declare game_num = int(clock*1000);
#declare game_num = 0;

#switch (3)
	#case (1) #declare game_board = < 9,  9, 10>; #break // Beginner
	#case (2) #declare game_board = <16, 16, 40>; #break // Intermediate
	#case (3) #declare game_board = <30, 16, 99>; #break // Expert
	#case (4) #declare game_board = <100, 100, 1000>; #break // Custom
#end

#declare hit_count      = 0;
#if (hit_count)
	#declare initial_hits = array[hit_count] { <12, 8> }
#end


///////////////////////////////////////////////////////////
// vars
#declare grid_seed      = seed(grid_num);
#declare game_seed      = seed(game_num);
#declare col            = game_board.x; 
#declare row            = game_board.y; 
#declare mines 	        = game_board.z;
#declare col_m          = col - 1;
#declare row_m          = row - 1;
#declare tables         = 4;
#declare gm             = 0;
#declare gr             = 1;
#declare max_loops      = 50;
#declare grid           = array[col][row][tables];
#declare hits           = 0;
#declare game_won       = false;
#declare total_changes  = 0;
#declare max_changes    = clock; // for animation, 0 = disabled
#declare rechanges      = 0;

///////////////////////////////////////////////////////////
//

camera {
  orthographic
  location <0,1,0>
  look_at  <0,0,0>
  right col*x
  up row*y
  translate <col/2, 0, row/2>
}

background { color rgb 0.5 }

#default { 
	finish { ambient 1 } 
}

#include "minesweeper.inc"


///////////////////////////////////////////////////////////
// Initialize grid
Init()


///////////////////////////////////////////////////////////
// Game play
#if (1)
	#declare game_won = false;
	#declare playing = true;
	#while (playing)

		NewHit()
		#debug concat("hit ",str(hits,2,0)," (",str(i,2,0),",",str(j,2,0),")\n")

		#if (IsMine(i, j)) // game over?
			#declare playing = false;
			#declare grid[i][j][gr] = 1;
			#declare grid[i][j][gm] = -2; // game ender

		#else
			#declare done = false;
			#declare loops = 0;
			#while (!done)
				CaptureSnapshot()
				
				ChangeTile(i, j, gr, 1)
								
				MatchBlank()
				MatchUnrevealed()
				MatchFlagged()
				MatchPatterns()
				
				#declare changes = CompareSnapshot();
				#debug concat("  loop changes: ",str(changes,3,0),"\n")
				#if (!changes)
					#declare done = true;
				#end
				
				#declare loops = loops + 1;
				#if (loops > max_loops)
					#debug "Max loops reached.\n"
					#declare done = true;
				#end

				#if ((max_changes) & (total_changes >= max_changes))
					#debug "Max changes reached.\n"
					#declare playing = false;
					#declare done = true;
				#end		 

			#end
		#end
		
		#if (CountFlaggedTiles() = mines)
			#declare playing = false;
			#declare game_won = true;
		#end

		#if (hits = hit_count)
			#declare playing = false;
		#end
	#end
#end


///////////////////////////////////////////////////////////
// output tiles
box { <0, 0, 0> <col, -1, row>
	pigment { rgb 1 }	
}

#declare i = 0; #while (i < col)
	#declare j = 0; #while (j < row)

		box { 
			0,<1, 0.1, 1>
			pigment { 
				image_map { png "tiles.png" }
				scale <13,1,1> 
				rotate 90*x 
				translate TileIcon(i, j)*x
			}
			translate <i, 0, j>
		}
		
	#declare j = j + 1; #end
#declare i = i + 1; #end


///////////////////////////////////////////////////////////
// 
#if (game_won)
	#declare msg = "WIN";
	#declare clr = rgbt <0, 0.4, 0, 0.6>;
#else
	#declare msg = "LOSE";
	#declare clr = rgbt <1, 0, 0, 0.6>;
#end

#if (0)
	text { ttf "timrom.ttf" msg 0.1 0
		pigment { clr }
		translate <0.4,0.125,0>
		scale <0.3*col, row, 1>
		rotate 90*x
		translate <0, 0.25, 0>
	}
#end

#debug concat("\n",msg)
#debug concat("\n  Grid number: ",str(grid_num,0,0))
#debug concat("\n  Game number: ",str(game_num,0,0))
#debug concat("\n         Hits: ",str(hits,0,0))
#debug concat("\nTotal changes: ",str(total_changes,0,0))
#debug concat("\n   Re-changes: ",str(rechanges,0,0),"\n")
