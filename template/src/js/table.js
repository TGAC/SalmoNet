$(function () {
    dtable = new webix.ui({
        container: "browsetable",
        id: "dtable",
        view: "datatable",
        columns: [
            {id: "uniprot", map: "#data1#", header: ["UniProt AC", {content: "textFilter"}], width: 100},
            {id: "genename", map: "#data2#", header: ["Gene name", {content: "textFilter"}], width: 200},
            {id: "locus", map: "#data3#", header: ["Locus", {content: "textFilter"}], width: 200},
            {id: "numort", map: "#data4#", header: "Othologs", width: 80},
            {id: "numint", map: "#data5#", header: "Interactions", width: 80}
        ],
        resizeColumn: true,
        datatype: "csv",
        url: data_url_prefix+'data/nodes.csv',
        autoheight: true,
        autowidth: true,
        pager: {
            template: "{common.prev()}{common.next()}Page {common.page()} from #limit#",
            container: "paging_here",
            size: 10,
            group: 5
        },
        hover: "browse_row_hover",
        on: {
            "onItemClick": function (id, e, trg) {
                window.location.href = data_url_prefix+"protein/"+dtable.getItem(id.row).uniprot+"/";
                // window.location.href = "uniprot.html";
                //webix.message("Click on row: "+dtable.getItem(id.row).uniprot);
            }
        }
    });
    webix.extend($$("dtable"), webix.ProgressBar);
    var strain_select = [
        {view: "label", label: "Select a strain:"},
        {
            view: "select",
            name: "strain",
            options: data_url_prefix+"data/strain_select.json"
        }];
    strain_select_form = new webix.ui({
        container: "strain_select_div",
        id: "strain_select_form",
        view: "form",
        scroll: false,
        width: 300,
        elements: strain_select
    });
    $$("strain_select_form").elements["strain"].attachEvent("onChange", function (newv, oldv) {
        $$("dtable").showProgress({
            type: "bottom",
            delay: 3000,
            hide: true
        });
        dtable.clearAll();
        dtable.load(data_url_prefix+"data/nodes" + newv + ".csv");
        $$("dtable").refresh();
        // webix.message("Value changed from: "+oldv+" to: "+newv);
    });
});
