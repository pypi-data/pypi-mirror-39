#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "Python.h"
// Includes all needed stuff.

typedef struct {
    char* ParsingString;
    int IgnoreQuotes;
    int HitAllArgs;
    char* LastParse;
} ArgParserStructure;
// The structure for the argument parser.

static ArgParserStructure ArgParser_Next(ArgParserStructure structure) {
    if (strcmp(structure.ParsingString, "") == 0) {
        structure.HitAllArgs = 1;
        return structure;
    }
    // Returns if all arguments have been hit.

    bool InQuotes = false;
    // Sets if the parser is inside quotes.

    char* CurrentParse = PyMem_Calloc((int) strlen(structure.ParsingString), 1);
    // Defines the current parse.

    char* *parsing_str = &structure.ParsingString;
    char current_char = *parsing_str[0];
    while (current_char != '\0') {
        switch (current_char) {
            case '"':
                if (InQuotes) {
                    // This is the end of some quoted text.
                    ++*parsing_str;
                    goto parse_done;
                }

                // Are we ignoring quotes?
                if (!structure.IgnoreQuotes) {
                    InQuotes = true;
                    break;
                }
            case ' ':
                if (!InQuotes) {
                    // Probably count this as a break.
                    if (strcmp(CurrentParse, "") == 0) {
                        break;
                    } else {
                        ++*parsing_str;
                        goto parse_done;
                    }
                }
            default:
                // Add this to the quote text.
                CurrentParse[(int) strlen(CurrentParse)] = current_char;
        }

        ++*parsing_str;
        current_char = *parsing_str[0];
        // Knocks off a character.
    }

    parse_done:
        structure.LastParse = PyMem_Malloc((int) strlen(CurrentParse) + 1);
        strcpy(structure.LastParse, CurrentParse);
        PyMem_Free(CurrentParse);
        return structure;
    // These are the instructions for when the parse is done.

    structure.ParsingString = "";
    goto parse_done;
    // All args done! Lets return the structure.
}
// Gets the next argument.
