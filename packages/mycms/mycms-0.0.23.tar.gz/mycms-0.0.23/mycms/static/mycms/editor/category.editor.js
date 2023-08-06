
function on() {
        console.log("Showing overlay");
    document.getElementById("overlay").style.display = "block";
}

function close_admin_overlay() {
    document.getElementById("overlay").style.display = "none";
}

$("#close-admin-overlay-button").click(function(){
        console.log("close-admin-overlay-button clicked");
        close_admin_overlay();
        });



function readCMSCategories(content_id){
/* Does a GET for the content and updates the editor textarea.

API Version 1 defines the endpoint as:

/cms/api/v1/cmscontents/{resource_id}/
*/
    console.log("readCMSContents called.");

    var id = view_json.id;
    url = "/cms/api/v2/cmsentries/"+  id + "/get_categories/";
    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
         }
    });
}


function getCMSCategories(content_id){
/** Does a GET for the content and updates the editor textarea.

API Version 1 defines the endpoint as:

/cms/api/v1/cmscontents/{resource_id}/
**/
    console.log("getCMSCategories called.");

    pk = view_json.id;
    //var pk=2;
    url = "/cms/api/v2/cmsentries/" + pk  + "/get_categories/";

    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
            content = data["categories"];
            console.log("DATA ", data);
            results = data["results"];
            console.log("RESULTS " + results );
                dust.render("yacms\/templates\/yacms\/dustjs_templates\/category_editor"
                            , { data: data }, function(err, out) {
                  // `out` contains the rendered output.
                  document.getElementById('category_editor').innerHTML= out;
                });
        }
    });

}


function string_to_slug (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    console.log(str);
    return str;
}

$(document).ready(function(){ 
    
    getCMSCategories(); 
    
    
    
});

$("#create_page_button").click(function(){
    console.log("yhou want to create a category");
    console.log($("#createpage_title").val());

        /* create the path. We need to post:
                1. current path + slug
                2. parent id
        */

        title = $("#createpage_title").val();
        slug = $("#createpage_slug").val();
        page_type = $('select[name=createpage_pagetype_select]').val();

        console.log(page_type);
        data = {
             title: title ,
             slug : slug,
             content: [ ],
             page_type: page_type,
            frontpage: false,
            published: false,
            page_number: 0
            };

        url = "/cms/api/v2/cmsentries/" + view_json.id + "/create_child/";
         $.ajax({
        url: url,
        type: 'POST',
        data: data,

        error: function(data){
            console.log("Category Child Creation Failed with error", data);
        },
        success: function(data){
            /**Update the editor for the newly created pages.**/
           console.log("Success");
           getCMSCategories();

        }
    });
});

$("#createpage_title").focusout(function(){
    console.log("createpage_title");
    console.log($("#createpage_title").val());

    var title = $("#createpage_title").val();
    var slug = string_to_slug(title);
    $("#createpage_slug").val(slug);
});


function appendCategoryRow(title, url){

  dust.render("yacms\/templates\/yacms\/dustjs_templates\/category_row", { data: data }, function(err, out) {
                   $("#"+category_entries).append(out);
                });

}


$("#save_content_button").click(function(){

    console.log("save_content_button pressed");

    console.log(view_json);
    console.log(view_json.content);
    var content_id = view_json.content[0];


    var content_txt = $("#category_texteditor_area").val();
    var start = Date.now();
    console.log(content_txt);
      $("#editor_message_pane").html("Saving content....");

    data = {   "content": content_txt,};

        url = "/cms/api/v2/cmscontents/" + content_id + "/";
         $.ajax({
        url: url,
        type: 'PUT',
        data: data,

        error: function(data){
            console.log("Failed to update content: ", data);
            $("#editor_message_pane").html("Failed to save  content with error:." + data);
        },
        success: function(data){
            /**Update the editor for the newly created pages.**/
           console.log("Success");
           var completed = Date.now()
           var seconds = ( completed - start)/1000;

           $("#editor_message_pane").html("Content was successfully saved..(" + seconds  + "s) "+ completed.toLocaleString());

        }
    });

    });


function getCMSContent(content_id){
/** Does a GET for the content and updates the editor textarea.

API Version 1 defines the endpoint as:

/cms/api/v1/cmscontents/{resource_id}/
**/
    console.log("getCMSContent called.");


    //var pk=2;
    url = "/cms/api/v2/cmscontents/" + content_id + "/";

    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){
            content = data["categories"];
            console.log("DATA ", data);

        }
    });

}


function loadCMSContentToTextArea(){
    /**

    Loads CMSContent entry as defined within the view_json that
    gets statically loaded into the page and then update the
    category.editor so that it can be edited.
    **/

    console.log("loadCMSContentToTextArea called");
    content_id = view_json.content[0];
    url = "/cms/api/v2/cmscontents/" + content_id + "/";

    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get cmscontent object");
        },
        success: function(data){

                console.log("loadCMSContentToTextArea");
                console.log("DATA ", data);

                $("#category_texteditor_area").val(data["content"]);

        }
    });

}


function getChildCMSEntries(){

    path_id = view_json.path;
    url = "/cms/api/v2/cmsentries/?limit=20&parent_path_id="+path_id;


    $.ajax({
        url: url,
        type: 'GET',
        error: function(){
            console.log("Failed to get CMSEntries");
        },
        success: function(data){
            console.log("ChildCMSEntries:", data);

            $('#CMSEntriesTable tbody').empty();

            results = data["results"];

            for (var i=0; i < results.length; i++){
                 entry = results[i];
                 table_row = "<tr><td>" + entry.id + "</td>";

                title_link = "<a href=\"/cms"+ entry.path + "\">" + entry.title + "</a>"

                table_row = table_row + "<td>" + title_link + "</td>";
                table_row = table_row + "<td>" + entry.page_type + "</td>";
                table_row = table_row + "<td>"+ entry.published +"</td>";
                table_row = table_row + "<td>"+ entry.frontpage +"</td>";
                table_row = table_row + "<td>"+ entry.date_created +"</td></tr>";

                console.log("Adding : " + table_row)

                $('#CMSEntriesTable tbody:last-child').append(table_row);


            }
        }
    });



}
