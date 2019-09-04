///////////////////////////////////////////////////////////
// Persistence of Vision Ray Tracer Scene Description File
// File: minesweeper.inc
// Vers: 3.6
// Desc: Macros for solving minesweeper
// Date: May 22, 2006
// Auth: David Curtis


///////////////////////////////////////////////////////////
// Type macros
#macro IsBlank     (i, j) (#if (grid[i][j][gm] =  0) true #else false #end) #end
#macro IsNumber    (i, j) (#if (grid[i][j][gm] >  0) true #else false #end) #end
#macro IsMine      (i, j) (#if (grid[i][j][gm] = -1) true #else false #end) #end
#macro IsUnrevealed(i, j) (#if (grid[i][j][gr] =  0) true #else false #end) #end
#macro IsRevealed  (i, j) (#if (grid[i][j][gr] =  1) true #else false #end) #end
#macro IsFlagged   (i, j) (#if (grid[i][j][gr] =  2) true #else false #end) #end


///////////////////////////////////////////////////////////
// Change Tile
#macro ChangeTile(i, j, table, value)
	#if ((max_changes = 0) | (total_changes < max_changes))
		#if (grid[i][j][table] != value)
			#declare grid[i][j][table] = value;
			#declare total_changes = total_changes + 1;
		#else
			#declare rechanges = rechanges + 1;
		#end
	#end
#end


///////////////////////////////////////////////////////////
// Initialize grid
#macro Init()
	// fill tables initially with zeros
	#declare i = 0; #while (i < col)
		#declare j = 0; #while (j < row)
			#declare k = 0; #while (k < tables)
				#declare grid[i][j][k] = 0;
			#declare k = k + 1; #end			
		#declare j = j + 1; #end
	#declare i = i + 1; #end
	
	
	// add random mines to grid 0
	#declare r = 0;
	#while (r < mines)
		#declare i = floor(rand(grid_seed) * col);
		#declare j = floor(rand(grid_seed) * row);
		#if (IsBlank(i, j))	
			#declare grid[i][j][gm] = -1;
			#declare r = r + 1; 
		#end
	#end
	
	
	// fill grid with count of adjacent mines
	#declare i = 0; #while (i < col)
		#declare j = 0; #while (j < row)
			#if (IsBlank(i, j))
				#declare grid[i][j][gm] = CountAdjacent_Mines(i, j);
			#end
		#declare j = j + 1; #end
	#declare i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// Get random unrevealed tile to hit
#macro NewHit()
	#if (hits < hit_count)
		#declare i = initial_hits[hits].x;
		#declare j = initial_hits[hits].y;
	#else
		#declare good = false;
		#while (!good)
			#declare i = floor(rand(game_seed) * col);
			#declare j = floor(rand(game_seed) * row);
			#if (IsUnrevealed(i, j))
				#declare good = true;
			#end
		#end
	#end
	#declare hits = hits + 1;
#end


///////////////////////////////////////////////////////////
// Return translation for tile in imagemap
#macro TileIcon(i, j)
	#switch (grid[i][j][gr])
		#case (0)
			#if (IsMine(i, j))
				#declare ti_index = 9;//12;                // mine (game over)
			#else
				#declare ti_index = 9;                     // unrevealed
			#end
			#break
		#case (2)
			#declare ti_index = 10;                      // flagged
			#break
		#else
			#switch (grid[i][j][gm])
				#range (1, 8)
					#declare ti_index = grid[i][j][gm] - 1;  // numbers
					#break
				#case (-1)
					#declare ti_index = 12;                  // mine
					#break
				#case (-2)
					#declare ti_index = 11;                  // mine hot
					#break
				#else
					#declare ti_index = 8;                   // blank
					#break
			#end
			#break
	#end
	-(ti_index)
#end


///////////////////////////////////////////////////////////
// Return count of adjacent mines, Used for Init not game
#macro CountAdjacent_Mines(i, j)
	#declare cam_cnt = 0;
	
	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)
			#if (IsMine(ip, jp)) 
				#declare cam_cnt = cam_cnt + 1;
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
	cam_cnt
#end


///////////////////////////////////////////////////////////
// Return count of all flags in grid
#macro CountFlaggedTiles()
	#declare cft_cnt = 0;
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#if (IsFlagged(i, j))
				#declare cft_cnt = cft_cnt + 1;
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
	cft_cnt
#end


///////////////////////////////////////////////////////////
// Return count of adjacent unrevealed tiles, not flagged
#macro CountAdjacent_Unrevealed(i, j)
	#declare cau_cnt = 0;
	
	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)
			#if (IsUnrevealed(ip, jp))
				#declare cau_cnt = cau_cnt + 1;
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
	cau_cnt
#end


///////////////////////////////////////////////////////////
// Return count of adjacent flagged tiles
#macro CountAdjacent_Flagged(i, j)
	#declare caf_cnt = 0;
	
	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)
			#if (IsFlagged(ip, jp)) 
				#declare caf_cnt = caf_cnt + 1;
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
	caf_cnt
#end


///////////////////////////////////////////////////////////
// Flag adjacent mines
#macro FlagAdjacentMines(i, j)
	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)
			#if (IsUnrevealed(ip, jp))
				ChangeTile(ip, jp, gr, 2)				
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
#end


///////////////////////////////////////////////////////////
// Reveal adjacent unflagged tiles
#macro RevealAdjacentTiles(i, j)
	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)
			#if (IsUnrevealed(ip, jp))
				ChangeTile(ip, jp, gr, 1)
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
#end


///////////////////////////////////////////////////////////
// Flag matching unrevealed tiles and numbers
#macro MatchUnrevealed()
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#if (IsNumber(i, j) & IsRevealed(i, j))
				#local mu_cnt = CountAdjacent_Unrevealed(i, j) + CountAdjacent_Flagged(i, j);
				#if (grid[i][j][gm] = mu_cnt)
					FlagAdjacentMines(i, j)
				#end
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// Scan for matching revealed numbers and flagged tiles
#macro MatchFlagged()
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#if (IsNumber(i, j) & IsRevealed(i, j))
				#local cnt = CountAdjacent_Flagged(i, j);
				#if (cnt = grid[i][j][gm])
					RevealAdjacentTiles(i, j)
				#end
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// Scan for revealed blanks with adjacent unrevealed tiles
#macro MatchBlank()
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#if (IsBlank(i, j) & IsRevealed(i, j))
				RevealAdjacentTiles(i, j)
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// List adjacent unrevealed tiles, return count
#declare lau1_list = array[8];
#declare lau2_list = array[8];
#macro ListAdjacent_Unrevealed(i, j, list)
	#declare lau_cnt = 0;

	#local is = #if (i = 0)     0;     #else i - 1; #end
	#local ie = #if (i = col_m) col_m; #else i + 1; #end
	#local js = #if (j = 0)     0;     #else j - 1; #end
	#local je = #if (j = row_m) row_m; #else j + 1; #end
	
	#local ip = is; #while (ip <= ie)
		#local jp = js; #while (jp <= je)			
			#if (!((ip = i) & (jp = j)))	
				#if (IsUnrevealed(ip, jp))	
					#if (list = 1)
						#declare lau1_list[lau_cnt] = <ip, jp>;
					#else
						#declare lau2_list[lau_cnt] = <ip, jp>;
					#end	
					#declare lau_cnt = lau_cnt + 1;
				#end
			#end
		#local jp = jp + 1; #end
	#local ip = ip + 1; #end
	lau_cnt
#end


///////////////////////////////////////////////////////////
// In list 1, return if tile is in lau1_list
#macro InLAUList1(i, j, c1)
	#declare ill1 = false;	
	#local r = 0;
	#while (r < c1)
		#if ((lau1_list[r].x = i) & (lau1_list[r].y = j))
			#declare ill1 = true;
		#end								
		#local r = r + 1;
	#end
	ill1
#end


///////////////////////////////////////////////////////////
// Compare lists, return count of matches
#macro CompareLAULists(c1, c2)
	#declare cll_cnt = 0;
	#local r = 0;
	#while (r < c2)
		#if (InLAUList1(lau2_list[r].x, lau2_list[r].y, c1))
			#declare cll_cnt = cll_cnt + 1;
		#end
		#local r = r + 1;
	#end
	cll_cnt	
#end


///////////////////////////////////////////////////////////
// Reveal non-matching tiles in list 2
#macro RevealLAUList2(c1, c2)
	#local r = 0;
	#while (r < c2)
		#if (!(InLAUList1(lau2_list[r].x, lau2_list[r].y, c1)))
			ChangeTile(lau2_list[r].x, lau2_list[r].y, gr, 1)
		#end
		#declare r = r + 1;		
	#end
#end


///////////////////////////////////////////////////////////
// Test is a number, unrevealed and missing flags
// return count of flags found else -1
#macro IsMissingFlags(i, j)
	#if (IsNumber(i, j) & IsRevealed(i, j))	
		#local imf_cnt = CountAdjacent_Flagged(i, j);
		#if (imf_cnt != grid[i][j][gm])
			#declare imf = imf_cnt;
		#else
			#declare imf = -1;			
		#end
	#else
		#declare imf = -1;
	#end
	imf
#end


///////////////////////////////////////////////////////////
// Scan for various patterns
// if the first tile matches all with the second
#macro MatchPatterns()
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
		
			#local m1_cnt = IsMissingFlags(i, j);
			#if (m1_cnt != -1)
					
				#local is = #if (i = 0)     0;     #else i - 1; #end
				#local ie = #if (i = col_m) col_m; #else i + 1; #end
				#local js = #if (j = 0)     0;     #else j - 1; #end
				#local je = #if (j = row_m) row_m; #else j + 1; #end
				
				#local ip = is; #while (ip <= ie)
					#local jp = js; #while (jp <= je)
											
					#if (!((ip = i) & (jp = j)))
						#local m2_cnt = IsMissingFlags(ip, jp);
						#if (m2_cnt != -1)
							#local t1_cnt = ListAdjacent_Unrevealed(i, j, 1);
							#local t2_cnt = ListAdjacent_Unrevealed(ip, jp, 2);
							#local match_cnt = CompareLAULists(t1_cnt, t2_cnt);
							#if (match_cnt = t1_cnt)
								#if (grid[ip][jp][gm] = m2_cnt + 1)
									RevealLAUList2(t1_cnt, t2_cnt)
								#end
							#end
						#end
					#end
					#local jp = jp + 1; #end
				#local ip = ip + 1; #end
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// Copy data in tables 0-1 to 2-3
#macro CaptureSnapshot()
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#declare grid[i][j][2] = grid[i][j][0];
			#declare grid[i][j][3] = grid[i][j][1];
		#local j = j + 1; #end
	#local i = i + 1; #end
#end


///////////////////////////////////////////////////////////
// Compare data in tables 0-1 to 2-3
// return true if matching
#macro CompareSnapshot()
	#declare cs = 0;
	#local i = 0; #while (i < col)
		#local j = 0; #while (j < row)
			#if ((grid[i][j][2] != grid[i][j][0]) | (grid[i][j][3] != grid[i][j][1]))
				#declare cs = cs + 1;
			#end
		#local j = j + 1; #end
	#local i = i + 1; #end
	cs
#end