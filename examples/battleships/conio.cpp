/** 
 * @file conio.cpp
 * @author Stefan Brandle/John Luscombe
 * @version 1.0
 * @date 2012/2018
 * @brief stubbed-out version of conio to make Aires happy
 *
 * This is the stubbed-out version of conio so Battleship players on Aires do
 * not blow up if they reference it.
 *
 * Definition/implementation of the console I/O functions
 *     Reference: http://en.wikipedia.org/wiki/ANSI_escape_code
 */ 

#ifndef CONIO_CPP
#define CONIO_CPP

#include <iostream>
#include <sstream>
#include "conio.h"

using namespace std;

/** @namespace conio
 *   The conio functions are not part of a class. They are just a set of functions
 *   collected within the conio namespace.
 */
namespace conio {

    /** @brief Positions cursor to the specified row, col location.
     *
     * Gotoxy will position the cursor at the specified row,col location. The upper left corner
     * has the coordinates 1,1. Note: this is row,col, not x,y (col,row) as is often done.
     *
     * @param row The row coordinate (1-based).
     * @param col The column coordinate (1-based).
     * @return Returns a string containing the escape sequence to send to the screen.
     * gotoRowCol = CSI r;c
     */
    string gotoRowCol( const int row, const int col ) {
	    return "";
    }

    const int Foreground = 1;	// local implementation-specific values
    const int Background = 2;

    string getColorSequence( Color c, int fgOrBg ) {
        return "";
    }

    /** @brief Returns a string that contains the escape sequence to set the
     * foreground color to the specified color.
     * @param c The Color valoue to use for the text foreground color.
     * @return A string containing the entire escape sequence to be output
     *     to the terminal to set the foreground color.
     */
    string fgColor( Color c ) {
	    return "";
    }

    /** @brief Returns a string that contains the escape sequence to set the
     * foreground color to the specified color.
     * @param c The Color valoue to use for the text background color.
     * @return A string containing the entire escape sequence to be output
     *     to the terminal to set the background color.
     */
    string bgColor( Color c ) {
        return "";
    }

    /** @brief Returns a string that contains the escape sequence to set the
     * text style to the specified TextStyle.
     * @param ts The TextStyle valoue to use for the text style.
     * @return A string containing the entire escape sequence to be output
     *     to the terminal to set the text style.
     */
    string setTextStyle( TextStyle ts ) {
        return "";
    }


    /** @brief Returns a string that contains the escape sequence to reset 
     * all the text attributes to default.
     * @return A string containing the entire escape sequence to be output
     *     to the terminal to reset text output to the default.
     */
    string resetAll( ) {
        return "";
    }

    /** @brief Returns a string that contains the escape sequence to clear
     * the screen.
     * @return A string containing the entire escape sequence to be output
     *     to the terminal to clear the screen.
     */
    string clrscr() {
        return "";
    }

}

#endif
