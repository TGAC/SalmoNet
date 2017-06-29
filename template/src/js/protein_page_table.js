$(document).ready(function(){
    interactiontablediv = webix.ui({
        container:"interactiontablediv",
        autowidth:true,
        rows: [
        {
            id: "interactiontable",
            view: "datatable",
            css: "salmonet_table",
            columns: [
                {id: "data0", header: ["Interactor", {content: "textFilter"}], css: "rank", adjust:true},
                {id: "data1", header: ["Interactor", {content: "textFilter"}], adjust:true},
                {id: "data2", header: "Source <a style='color: #1F2421 !important;' href='#legend' class='uk-icon-justify uk-icon-question-circle'></a>", fillspace:true},
                {id: "data3", header: ["Layer", {content: "selectFilter"}], adjust:true},
                {id: "data4", hidden:true},
                {id: "data5", hidden:true},
                {id: "data6", hidden:true},
                {id: "data7", hidden:true},
                {id: "data8", hidden:true},
                {id: "data9", hidden:true},
                {id: "data10", hidden:true},
                {id: "data11", hidden:true}
            ],
            height: 450,
            autowidth:true,
            datatype: "csv",
            data: document.getElementById('interactiontabledata').value
            // data: '{{ .Params.interactioncsv | safeHTML }}'
        },
        {
            view: "form",
            css: "toolbar",
            paddingY: 5,
            paddingX: 10,
            autowidth:true,
            cols:[
                {
                    view: "button", label: "Download table", width: 200, click:function(){
                        webix.toExcel($$("interactiontable"), {
                            filename: "SalmoNet_{{ .Params.uniprot }}",
                            name: "{{ .Params.genename }}",
                            columns:{
                                "data0":{header: "node_a_genename"},
                                "data1":{header: "node_b_genename"},
                                "data2":{header: "source"},
                                "data3":{header: "layer"},
                                "data4":{header: "node_a_locus"},
                                "data5":{header: "node_b_locus"},
                                "data6":{header: "node_a_uniprot"},
                                "data7":{header: "node_b_uniprot"},
                                "data8":{header: "node_a_ortholog_group"},
                                "data9":{header: "node_b_ortholog_group"},
                                "data10":{header: "node_a_strain"},
                                "data11":{header: "node_b_strain"}
                            }
                        });
                    }
                }
            ]
        }]
    });
    if ($(window).width() < 850){
        $$('interactiontable').hideColumn("data2");
        // $$('interactiontable').setColumnWidth("data0", 80);
        // $$('interactiontable').setColumnWidth("data1", 80);
    };
});

$(window).resize(function() {
    if ($(window).width() < 850){
        $$('interactiontable').hideColumn("data2");
        // $$('interactiontable').setColumnWidth("data0", 80);
        // $$('interactiontable').setColumnWidth("data1", 80);
        // $$('interactiontable').setColumnWidth("data3", 100);
    }
    if ($(window).width() >= 850){
        $$('interactiontable').showColumn("data2");
        // $$('interactiontable').setColumnWidth("data0", 100);
        // $$('interactiontable').setColumnWidth("data1", 100);
        // $$('interactiontable').setColumnWidth("data3", 150);
    }
});
// interactiontablediv.define("width", $("#interactiontablediv").width());
// interactiontablediv.resize();
// $(window).resize(function() {
//     interactiontablediv.define("width", $("#interactiontablediv").width());
//     interactiontablediv.resize();
// });
// $$('interactiontable').define("width", $("#interactiontablediv").width());
// $$('interactiontable').resize();
// $(window).resize(function() {
//     $$('interactiontable').define("width", $("#interactiontablediv").width());
//     $$('interactiontable').resize();
// });
