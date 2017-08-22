Parser for  KRISHA.KZ site
No class, only functions. Used simple names, to clearly understand the code.

Definition of each function:

//Taking a link, parsing html page from this link, returns a string in a given format with delimiter --> |
parse_data


//Getting links of all adverts in the page, returns an array of links (strings)
pulling_links


//Getting count of all adverts in given city, returns an int number
get_count


//Getting whole links from given city (This function contains pulling_links and normalizing_links functions)
get_links


//Adding for each link (it is looks like: a/show/*****) its accurate link (making it more readable: https://krisha.kz/a/show/*****)
normalizing_links


//Saving links to a file (Name specified during the process, like : links_almaty.txt)
save_links


//Saving data to a file (Name specified during the process, like: data_almaty.txt)
//Need to change it to save data to the DB
save_data


//Writing a logs
log


//Parsing pages from first index to the second (and saving it, using the save_data function)
parse_and_save


//Start function, static cities to parse (list from krisha.kz)
cities


//Main function
main
