/**/

/*
 Highcharts JS v4.1.7 (2015-06-26)
 Exporting module

 (c) 2010-2014 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(f){var z=f.Chart,s=f.addEvent,A=f.removeEvent,B=HighchartsAdapter.fireEvent,j=f.createElement,p=f.discardElement,u=f.css,l=f.merge,m=f.each,q=f.extend,E=f.splat,F=Math.max,k=document,C=window,G=f.isTouchDevice,H=f.Renderer.prototype.symbols,r=f.getOptions(),x;q(r.lang,{printChart:"Print chart",downloadPNG:"Download PNG image",downloadJPEG:"Download JPEG image",downloadPDF:"Download PDF document",downloadSVG:"Download SVG vector image",contextButtonTitle:"Chart context menu"});r.navigation=
{menuStyle:{border:"1px solid #A0A0A0",background:"#FFFFFF",padding:"5px 0"},menuItemStyle:{padding:"0 10px",background:"none",color:"#303030",fontSize:G?"14px":"11px"},menuItemHoverStyle:{background:"#4572A5",color:"#FFFFFF"},buttonOptions:{symbolFill:"#E0E0E0",symbolSize:14,symbolStroke:"#666",symbolStrokeWidth:3,symbolX:12.5,symbolY:10.5,align:"right",buttonSpacing:3,height:22,theme:{fill:"white",stroke:"none"},verticalAlign:"top",width:24}};r.exporting={type:"image/png",url:"http://export.highcharts.com/",
buttons:{contextButton:{menuClassName:"highcharts-contextmenu",symbol:"menu",_titleKey:"contextButtonTitle",menuItems:[{textKey:"printChart",onclick:function(){this.print()}},{separator:!0},{textKey:"downloadPNG",onclick:function(){this.exportChart()}},{textKey:"downloadJPEG",onclick:function(){this.exportChart({type:"image/jpeg"})}},{textKey:"downloadPDF",onclick:function(){this.exportChart({type:"application/pdf"})}},{textKey:"downloadSVG",onclick:function(){this.exportChart({type:"image/svg+xml"})}}]}}};
f.post=function(b,a,e){var c,b=j("form",l({method:"post",action:b,enctype:"multipart/form-data"},e),{display:"none"},k.body);for(c in a)j("input",{type:"hidden",name:c,value:a[c]},null,b);b.submit();p(b)};q(z.prototype,{sanitizeSVG:function(b){return b.replace(/zIndex="[^"]+"/g,"").replace(/isShadow="[^"]+"/g,"").replace(/symbolName="[^"]+"/g,"").replace(/jQuery[0-9]+="[^"]+"/g,"").replace(/url\([^#]+#/g,"url(#").replace(/<svg /,'<svg xmlns:xlink="http://www.w3.org/1999/xlink" ').replace(/ (NS[0-9]+\:)?href=/g,
" xlink:href=").replace(/\n/," ").replace(/<\/svg>.*?$/,"</svg>").replace(/(fill|stroke)="rgba\(([ 0-9]+,[ 0-9]+,[ 0-9]+),([ 0-9\.]+)\)"/g,'$1="rgb($2)" $1-opacity="$3"').replace(/&nbsp;/g," ").replace(/&shy;/g,"­").replace(/<IMG /g,"<image ").replace(/<(\/?)TITLE>/g,"<$1title>").replace(/height=([^" ]+)/g,'height="$1"').replace(/width=([^" ]+)/g,'width="$1"').replace(/hc-svg-href="([^"]+)">/g,'xlink:href="$1"/>').replace(/ id=([^" >]+)/g,' id="$1"').replace(/class=([^" >]+)/g,'class="$1"').replace(/ transform /g,
" ").replace(/:(path|rect)/g,"$1").replace(/style="([^"]+)"/g,function(a){return a.toLowerCase()})},getSVG:function(b){var a=this,e,c,g,y,h,d=l(a.options,b);if(!k.createElementNS)k.createElementNS=function(a,b){return k.createElement(b)};c=j("div",null,{position:"absolute",top:"-9999em",width:a.chartWidth+"px",height:a.chartHeight+"px"},k.body);g=a.renderTo.style.width;h=a.renderTo.style.height;g=d.exporting.sourceWidth||d.chart.width||/px$/.test(g)&&parseInt(g,10)||600;h=d.exporting.sourceHeight||
d.chart.height||/px$/.test(h)&&parseInt(h,10)||400;q(d.chart,{animation:!1,renderTo:c,forExport:!0,width:g,height:h});d.exporting.enabled=!1;delete d.data;d.series=[];m(a.series,function(a){y=l(a.options,{animation:!1,enableMouseTracking:!1,showCheckbox:!1,visible:a.visible});y.isInternal||d.series.push(y)});b&&m(["xAxis","yAxis"],function(a){m(E(b[a]),function(b,c){d[a][c]=l(d[a][c],b)})});e=new f.Chart(d,a.callback);m(["xAxis","yAxis"],function(b){m(a[b],function(a,d){var c=e[b][d],g=a.getExtremes(),
h=g.userMin,g=g.userMax;c&&(h!==void 0||g!==void 0)&&c.setExtremes(h,g,!0,!1)})});g=e.container.innerHTML;d=null;e.destroy();p(c);g=this.sanitizeSVG(g);return g=g.replace(/(url\(#highcharts-[0-9]+)&quot;/g,"$1").replace(/&quot;/g,"'")},getSVGForExport:function(b,a){var e=this.options.exporting;return this.getSVG(l({chart:{borderRadius:0}},e.chartOptions,a,{exporting:{sourceWidth:b&&b.sourceWidth||e.sourceWidth,sourceHeight:b&&b.sourceHeight||e.sourceHeight}}))},exportChart:function(b,a){var e=this.getSVGForExport(b,
a),b=l(this.options.exporting,b);f.post(b.url,{filename:b.filename||"chart",type:b.type,width:b.width||0,scale:b.scale||2,svg:e},b.formAttributes)},print:function(){var b=this,a=b.container,e=[],c=a.parentNode,g=k.body,f=g.childNodes;if(!b.isPrinting)b.isPrinting=!0,B(b,"beforePrint"),m(f,function(a,b){if(a.nodeType===1)e[b]=a.style.display,a.style.display="none"}),g.appendChild(a),C.focus(),C.print(),setTimeout(function(){c.appendChild(a);m(f,function(a,b){if(a.nodeType===1)a.style.display=e[b]});
b.isPrinting=!1;B(b,"afterPrint")},1E3)},contextMenu:function(b,a,e,c,g,f,h){var d=this,l=d.options.navigation,D=l.menuItemStyle,n=d.chartWidth,o=d.chartHeight,k="cache-"+b,i=d[k],t=F(g,f),v,w,p,r=function(a){d.pointer.inClass(a.target,b)||w()};if(!i)d[k]=i=j("div",{className:b},{position:"absolute",zIndex:1E3,padding:t+"px"},d.container),v=j("div",null,q({MozBoxShadow:"3px 3px 10px #888",WebkitBoxShadow:"3px 3px 10px #888",boxShadow:"3px 3px 10px #888"},l.menuStyle),i),w=function(){u(i,{display:"none"});
h&&h.setState(0);d.openMenu=!1},s(i,"mouseleave",function(){p=setTimeout(w,500)}),s(i,"mouseenter",function(){clearTimeout(p)}),s(document,"mouseup",r),s(d,"destroy",function(){A(document,"mouseup",r)}),m(a,function(a){if(a){var b=a.separator?j("hr",null,null,v):j("div",{onmouseover:function(){u(this,l.menuItemHoverStyle)},onmouseout:function(){u(this,D)},onclick:function(){w();a.onclick&&a.onclick.apply(d,arguments)},innerHTML:a.text||d.options.lang[a.textKey]},q({cursor:"pointer"},D),v);d.exportDivElements.push(b)}}),
d.exportDivElements.push(v,i),d.exportMenuWidth=i.offsetWidth,d.exportMenuHeight=i.offsetHeight;a={display:"block"};e+d.exportMenuWidth>n?a.right=n-e-g-t+"px":a.left=e-t+"px";c+f+d.exportMenuHeight>o&&h.alignOptions.verticalAlign!=="top"?a.bottom=o-c-t+"px":a.top=c+f-t+"px";u(i,a);d.openMenu=!0},addButton:function(b){var a=this,e=a.renderer,c=l(a.options.navigation.buttonOptions,b),g=c.onclick,k=c.menuItems,h,d,m={stroke:c.symbolStroke,fill:c.symbolFill},j=c.symbolSize||12;if(!a.btnCount)a.btnCount=
0;if(!a.exportDivElements)a.exportDivElements=[],a.exportSVGElements=[];if(c.enabled!==!1){var n=c.theme,o=n.states,p=o&&o.hover,o=o&&o.select,i;delete n.states;g?i=function(){g.apply(a,arguments)}:k&&(i=function(){a.contextMenu(d.menuClassName,k,d.translateX,d.translateY,d.width,d.height,d);d.setState(2)});c.text&&c.symbol?n.paddingLeft=f.pick(n.paddingLeft,25):c.text||q(n,{width:c.width,height:c.height,padding:0});d=e.button(c.text,0,0,i,n,p,o).attr({title:a.options.lang[c._titleKey],"stroke-linecap":"round"});
d.menuClassName=b.menuClassName||"highcharts-menu-"+a.btnCount++;c.symbol&&(h=e.symbol(c.symbol,c.symbolX-j/2,c.symbolY-j/2,j,j).attr(q(m,{"stroke-width":c.symbolStrokeWidth||1,zIndex:1})).add(d));d.add().align(q(c,{width:d.width,x:f.pick(c.x,x)}),!0,"spacingBox");x+=(d.width+c.buttonSpacing)*(c.align==="right"?-1:1);a.exportSVGElements.push(d,h)}},destroyExport:function(b){var b=b.target,a,e;for(a=0;a<b.exportSVGElements.length;a++)if(e=b.exportSVGElements[a])e.onclick=e.ontouchstart=null,b.exportSVGElements[a]=
e.destroy();for(a=0;a<b.exportDivElements.length;a++)e=b.exportDivElements[a],A(e,"mouseleave"),b.exportDivElements[a]=e.onmouseout=e.onmouseover=e.ontouchstart=e.onclick=null,p(e)}});H.menu=function(b,a,e,c){return["M",b,a+2.5,"L",b+e,a+2.5,"M",b,a+c/2+0.5,"L",b+e,a+c/2+0.5,"M",b,a+c-1.5,"L",b+e,a+c-1.5]};z.prototype.callbacks.push(function(b){var a,e=b.options.exporting,c=e.buttons;x=0;if(e.enabled!==!1){for(a in c)b.addButton(c[a]);s(b,"destroy",b.destroyExport)}})})(Highcharts);

/**
 * A Highcharts plugin for exporting data from a rendered chart as CSV, XLS or HTML table
 *
 * Author:   Torstein Honsi
 * Licence:  MIT
 * Version:  1.3.5
 */
/*global Highcharts, window, document, Blob */
(function (Highcharts) {

    'use strict';

    var each = Highcharts.each,
        downloadAttrSupported = document.createElement('a').download !== undefined;

    Highcharts.setOptions({
        lang: {
            downloadCSV: 'Download CSV',
            downloadXLS: 'Download XLS'
        }
    });


    /**
     * Get the data rows as a two dimensional array
     */
    Highcharts.Chart.prototype.getDataRows = function () {
        var options = (this.options.exporting || {}).csv || {},
            xAxis = this.xAxis[0],
            rows = {},
            rowArr = [],
            dataRows,
            names = [],
            i,
            x,

            // Options
            dateFormat = options.dateFormat || '%Y-%m-%d %H:%M:%S';

        // Loop the series and index values
        i = 0;
        each(this.series, function (series) {
            var keys = series.options.keys,
                pointArrayMap = keys || series.pointArrayMap || ['y'],
                valueCount = pointArrayMap.length,
                j;

            if (series.options.includeInCSVExport !== false && series.visible !== false) { // #55
                names.push(series.name);

                each(series.points, function (point) {
                    j = 0;
                    if (!rows[point.x]) {
                        rows[point.x] = [];
                    }
                    rows[point.x].x = point.x;

                    // Pies, funnels etc. use point name in X row
                    if (!series.xAxis) {
                        rows[point.x].name = point.name;
                    }

                    while (j < valueCount) {
                        rows[point.x][i + j] = point[pointArrayMap[j]];
                        j = j + 1;
                    }

                });
                i = i + j;
            }
        });

        // Make a sortable array
        for (x in rows) {
            if (rows.hasOwnProperty(x)) {
                rowArr.push(rows[x]);
            }
        }
        // Sort it by X values
        rowArr.sort(function (a, b) {
            return a.x - b.x;
        });

        // Add header row
        dataRows = [[xAxis.isDatetimeAxis ? 'DateTime' : 'Category'].concat(names)];

        // Transform the rows to CSV
        each(rowArr, function (row) {

            var category = row.name;
            if (!category) {
                if (xAxis.isDatetimeAxis) {
                    category = Highcharts.dateFormat(dateFormat, row.x);
                } else if (xAxis.categories) {
                    category = Highcharts.pick(xAxis.names[row.x], xAxis.categories[row.x], row.x)
                } else {
                    category = row.x;
                }
            }

            // Add the X/date/category
            row.unshift(category);
            dataRows.push(row);
        });

        return dataRows;
    };

    /**
     * Get a CSV string
     */
    Highcharts.Chart.prototype.getCSV = function (useLocalDecimalPoint) {
        var csv = '',
            rows = this.getDataRows(),
            options = (this.options.exporting || {}).csv || {},
            itemDelimiter = options.itemDelimiter || ',', // use ';' for direct import to Excel
            lineDelimiter = options.lineDelimiter || '\n'; // '\n' isn't working with the js csv data extraction

        // Transform the rows to CSV
        each(rows, function (row, i) {
            var val = '',
                j = row.length,
                n = useLocalDecimalPoint ? (1.1).toLocaleString()[1] : '.';
            while (j--) {
                val = row[j];
                if (typeof val === "string") {
                    val = '"' + val + '"';
                }
                if (typeof val === 'number') {
                    if (n === ',') {
                        val = val.toString().replace(".", ",");
                    }
                }
                row[j] = val;
            }
            // Add the values
            csv += row.join(itemDelimiter);

            // Add the line delimiter
            if (i < rows.length - 1) {
                csv += lineDelimiter;
            }
        });
        return csv;
    };

    /**
     * Build a HTML table with the data
     */
    Highcharts.Chart.prototype.getTable = function (useLocalDecimalPoint) {
        var html = '<table>',
            rows = this.getDataRows();

        // Transform the rows to HTML
        each(rows, function (row, i) {
            var tag = i ? 'td' : 'th',
                val,
                j,
                n = useLocalDecimalPoint ? (1.1).toLocaleString()[1] : '.';

            html += '<tr>';
            for (j = 0; j < row.length; j = j + 1) {
                val = row[j];
                // Add the cell
                if (typeof val === 'number') {
                    if (n === ',') {
                        html += '<' + tag + (typeof val === 'number' ? ' class="number"' : '') + '>' + val.toString().replace(".", ",") + '</' + tag + '>';
                    } else {
                        html += '<' + tag + (typeof val === 'number' ? ' class="number"' : '') + '>' + val.toString() + '</' + tag + '>';
                    }
                } else {
                    html += '<' + tag + '>' + val + '</' + tag + '>';
                }
            }

            html += '</tr>';
        });
        html += '</table>';
        return html;
    };

    function getContent(chart, href, extension, content, MIME) {
        var a,
            blobObject,
            name = (chart.title ? chart.title.textStr.replace(/ /g, '-').toLowerCase() : 'chart'),
            options = (chart.options.exporting || {}).csv || {},
            url = options.url || 'http://www.highcharts.com/studies/csv-export/download.php';

        // Download attribute supported
        if (downloadAttrSupported) {
            a = document.createElement('a');
            a.href = href;
            a.target      = '_blank';
            a.download    = name + '.' + extension;
            document.body.appendChild(a);
            a.click();
            a.remove();

        } else if (window.Blob && window.navigator.msSaveOrOpenBlob) {
            // Falls to msSaveOrOpenBlob if download attribute is not supported
            blobObject = new Blob([content]);
            window.navigator.msSaveOrOpenBlob(blobObject, name + '.' + extension);

        } else {
            // Fall back to server side handling
            Highcharts.post(url, {
                data: content,
                type: MIME,
                extension: extension
            });
        }
    }

    /**
     * Call this on click of 'Download CSV' button
     */
    Highcharts.Chart.prototype.downloadCSV = function () {
        var csv = this.getCSV(true);
        getContent(
            this,
            'data:text/csv,\uFEFF' + csv.replace(/\n/g, '%0A'),
            'csv',
            csv,
            'text/csv'
        );
    };

    /**
     * Call this on click of 'Download XLS' button
     */
    Highcharts.Chart.prototype.downloadXLS = function () {
        var uri = 'data:application/vnd.ms-excel;base64,',
            template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40">' +
                '<head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>' +
                '<x:Name>Ark1</x:Name>' +
                '<x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]-->' +
                '<style>td{border:none;font-family: Calibri, sans-serif;} .number{mso-number-format:"0.00";}</style>' +
                '<meta name=ProgId content=Excel.Sheet>' +
                '</head><body>' +
                this.getTable(true) +
                '</body></html>',
            base64 = function (s) { 
                return window.btoa(unescape(encodeURIComponent(s))); // #50
            };
        getContent(
            this,
            uri + base64(template),
            'xls',
            template,
            'application/vnd.ms-excel'
        );
    };


    // Add "Download CSV" to the exporting menu. Use download attribute if supported, else
    // run a simple PHP script that returns a file. The source code for the PHP script can be viewed at
    // https://raw.github.com/highslide-software/highcharts.com/master/studies/csv-export/csv.php
    if (Highcharts.getOptions().exporting) {
        Highcharts.getOptions().exporting.buttons.contextButton.menuItems.push({
            textKey: 'downloadCSV',
            onclick: function () { this.downloadCSV(); }
        }, {
            textKey: 'downloadXLS',
            onclick: function () { this.downloadXLS(); }
        });
    }

}(Highcharts));

var doneFlag=false;var failFlag=false;var liveMinDate=$("#minLiveDate").val();var accessControl=$("#accessControl").val();$.each($(".enable-when-done"),function(a,b){$(b).css("color","#999");$(b).css("cursor","default")});function getSourceCode($dom){if($dom.attr("_isLoad")=="0"){if(accessControl==1){if(!g_isWinApp||typeof jsObj=="undefined"){return"#请在客户端打开查看源码"}else{var backtestId=$("#backtestId").attr("backtestId_");var res=jsObj.ReadBacktestCode(backtestId);var obj=eval("("+res+")");if(obj.code!="00000"){return"#无法查看源码"+obj.msg}$dom.text(obj.data)}}else{var id=$dom.attr("_backtestId");Cy.ajax("/algorithm/backtest/source",{async:false,data:{backtestId:id},success:function(res){$dom.text(res.data.source);$dom.attr("_isLoad","1")}})}}return $dom.text()}$("#view-code-button").click(function(){BootstrapDialog.show({title:"策略代码",btnOKLabel:"确认",cssClass:"code-dialog",message:"",onshown:function(b){var e=$(".bootstrap-dialog-message").eq(0);e.attr("id","code-view");var a=$("body").height()*0.7;e.css("height",a+"px");var d=getSourceCode($("#code"));e.text(d);$(".code-dialog .modal-dialog").css("width","700px");var c=ace.edit("code-view");c.session.setMode("ace/mode/python");c.setTheme("ace/theme/tomorrow")},data:{id:"code-dialog"}})});$("#view-detail-button").click(function(){BootstrapDialog.show({title:"回测详情",btnOKLabel:"确认",message:$("#backtest-detail").html().replace(/(\n)+|(\r\n)+/g,"")})});$("#export-chart-button").click(function(){if(chart){chart.exportChart()}});$("#export-csv-button").click(function(){if(chart){window.location.href="/algorithm/backtest/export?backtestId="+backtestId+"&type=result"}});$(".popover-right").popover({placement:"bottom",trigger:"manual",html:true,content:'风险指标有利于您对策略进行客观的评价，<a target="_blank" style="color:#337ab7;font-weight:normal" href="/api#%E9%A3%8E%E9%99%A9%E6%8C%87%E6%A0%87">查看计算公式</a>'}).on("mouseenter",function(){var a=this;$(this).popover("show");$(this).siblings(".popover").on("mouseleave",function(){$(a).popover("hide")})}).on("mouseleave",function(){var a=this;setTimeout(function(){if(!$(".popover:hover").length){$(a).popover("hide")}},100)});updateResultSize();$(window).resize(function(){updateResultSize()});function updateResultSize(){var a=$("#backtest-atomic-container").width()-$("#result-area").width()-40;if(!$("body").hasClass("mobile")){$("#splitter-pane").width(a)}}$("#result-tabs  a").click(function(){if($(this).hasClass("enable-when-done")&&!doneFlag){return false}$(".dailybars-output .active").addClass("hidden");var a=$(this).attr("href").toString();$(a).removeClass("hidden");if(a=="#tab-transactioninfo"&&$(a).attr("_hasDrawn")==0){fillTransaction()}else{if(a=="#tab-positioninfo"&&$(a).attr("_hasDrawn")==0){fillPosition()}else{if($(this).hasClass("risk")&&$(a).attr("_hasDrawn")==0){fillRisk()}else{if(a=="#tab-logs"&&$(a).attr("_hasDrawn")==0){fillLog()}else{if(a=="#tab-profile"&&$(a).attr("_hasDrawn")==0){fillProfile()}}}}}});$("#cancel-backtest-button").click(function(){BootstrapDialog.confirm({title:"提示",btnCancelLabel:"取消",btnOKLabel:"确认",message:"确实要取消?",callback:function(a){if(a){cancel()}else{}}})});function cancel(){Cy.ajax("/algorithm/index/cancel",{data:"backtestId="+backtestId,async:false,success:function(a){stopCycle=true;$("#detail-finished").html("已取消");$("#backtest-complete").html('<i class="icon icon-remove"></i> 已取消');$("#done-backtest-pane").removeClass("hidden");$("#inprogress-backtest-pane").addClass("hidden");$.each($(".enable-when-done"),function(b,c){$(c).css("color","#333");$(c).css("cursor","pointer")});return false},fail:function(a){BootstrapDialog.show({title:"提示",btnOKLabel:"确认",message:"无法取消:"+a.msg})}})}var chart;var resultOffset=0;var userRecordOffset=0;var logOffset=0;var errorLogOffset=0;var frequency=$("#frequency").attr("value");var stopCycle=false;var stopResult=false;var backtestId=$("#backtestId").val();var dataResult=[];var dataBenchmark=[];var excessResult=[];var dataGains={earn:[],lose:[]};var dataOrders={buy:[],sell:[]};var origDataOffset=0;var userRecord=null;var startDate=$("#startDate").html();var endDate=$("#endDate").html();var minY=0;var chartType="line";Highcharts.setOptions({global:{timezoneOffset:-8*60},lang:{months:["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],shortMonths:["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],weekdays:["星期天","星期一","星期二","星期三","星期四","星期五","星期六"],rangeSelectorZoom:"缩放：",rangeSelectorFrom:"从",rangeSelectorTo:"到"}});var timeoutSpan=3000;function cycleCheck(){if(stopCycle){return}if(stopResult==false){drawResult(backtestId)}setTimeout(cycleCheck,timeoutSpan)}function fillStatsExtraHtml(a){if(a.data.win_ratio){$("#win_ratio").html(a.data.win_ratio.toFixed(3))}if(a.data.day_win_ratio){$("#day_win_ratio").html(a.data.day_win_ratio.toFixed(3))}if(a.data.profit_loss_ratio){$("#profit_loss_ratio").html(a.data.profit_loss_ratio.toFixed(3))}if(a.data.win_count){$("#win_count").html(a.data.win_count)}if(a.data.lose_count){$("#lose_count").html(a.data.lose_count)}}function fillStatsExtra(){if(backtestId<1750000){return}Cy.ajax("/algorithm/backtest/stats?backtestId="+backtestId,{success:function(a){if(!a.data){setTimeout(fillStatsExtra,500);return}if(typeof a.data.win_ratio=="undefined"){setTimeout(fillStatsExtra,2000);return}fillStatsExtraHtml(a)}})}function fillStats(){Cy.ajax("/algorithm/backtest/stats?backtestId="+backtestId,{success:function(b){if(!b.data){setTimeout(fillStats,500);return}var c=(startDate.substring(0,4));var e=(startDate.substring(5,7)-1);var a=(startDate.substring(8,10));var g=new Date(c,e,a,0,0,0).getTime();c=(endDate.substring(0,4));e=(endDate.substring(5,7)-1);a=(endDate.substring(8,10));if(!b.data.annual_algo_return){var c=b.data.trading_days/250;var f=Math.pow((1+b.data.algorithm_return),1/c)-1}else{var f=b.data.annual_algo_return}$("#year_returns").html((f*100).toFixed(2)+"%");$("#total_returns").html((b.data.algorithm_return*100).toFixed(2)+"%");$("#benchmark_returns").html((b.data.benchmark_return*100).toFixed(2)+"%");$("#alpha").html(b.data.alpha.toFixed(3));$("#beta").html(b.data.beta.toFixed(3));$("#sharpe").html(b.data.sharpe.toFixed(3));$("#sortino").html(b.data.sortino.toFixed(3));$("#information").html(b.data.information.toFixed(3));$("#algorithm_volatility").html(b.data.algorithm_volatility.toFixed(3));$("#benchmark_volatility").html(b.data.benchmark_volatility.toFixed(3));if(typeof b.data.win_ratio=="undefined"){fillStatsExtra()}else{fillStatsExtraHtml(b)}var d=(b.data.max_drawdown*100).toFixed(3)+"%";if(b.data.max_drawdown_period){d=d+'<span style="font-size:11px;">('+b.data.max_drawdown_period[0]+","+b.data.max_drawdown_period[1]+")</span>";chart.addSeries({type:"flags",data:[{x:Date.parse(new Date(b.data.max_drawdown_period[0])),title:" ",text:"最大回撤"},{x:Date.parse(new Date(b.data.max_drawdown_period[1])),title:" ",text:"最大回撤"}],onSeries:"returnseries",fillColor:"#00BB00",states:{hover:{fillColor:"#00BB00"}},shape:"circlepin",y:-3,height:4,width:4})}$("#max_drawdown").html(d);if(b.data.report_done_seconds){$("#run-time-cost").html(" , 耗时"+b.data.report_done_seconds.toFixed(2)+"s")}}})}function fillLog(a){if(typeof a==undefined){a=0}Cy.ajax("/algorithm/backtest/log?backtestId="+backtestId+"&offset="+logOffset,{success:function(h){if(h.data.logArr.length==0&&(h.data.state==2||h.data.state==3)){return}if(h.data.offset<logOffset){return}if(logOffset==0){$("#logs-init").addClass("hidden");$("#log").scroll(function(){nScrollHight=$(this)[0].scrollHeight;a=$(this)[0].scrollTop;if(a+570>=nScrollHight){fillLog(a)}})}var g="";for(var f=0;f<h.data.logArr.length;f++){if(!h.data.logArr[f]){continue}var e=h.data.logArr[f].split(" - ");if(e.length>2){var c='<span class="log-date">'+e[0]+"</span> - ";if(e[1]=="ERROR"){var j="log-error"}else{if(e[1]=="WARNING"){var j="log-warning"}else{var j="log-info"}}var b='<span class="'+j+'">'+e[1]+"</span> - ";e.shift();e.shift();var d=c+b+e.join("-")}else{var d=h.data.logArr[f]}g=g+"<p>"+d.replace(/\n/g,"<br/>");+"</p>";logOffset++}$("#log").find("pre").eq(0).append(g);$("#id").scrollTop(a)}})}function fillErrorLog(a){Cy.ajax("/algorithm/backtest/error?backtestId="+a,{success:function(d){var c="";for(var b=0;b<d.data.logArr.length;b++){c=c+"<p>"+d.data.logArr[b].replace(/\n/g,"<br/>");+"</p>";errorLogOffset++}$("#log").find("pre").eq(0).prepend(c)}})}function fillProfile(){Cy.ajax("/algorithm/backtest/profile?backtestId="+backtestId,{success:function(b){if(b.data.profile&&b.data.profile.length>0){$("#profile").find("pre").eq(0).append(b.data.profile)}else{var a="暂无相关内容，请确认在代码最开始使用enable_profile()打开性能分析。<a href='/api#enableprofile'  style='color:#337ab7' target='_blank'>查看enable_profile()使用方法</a>";$("#profile").find("pre").eq(0).append(a)}$("#tab-profile").attr("_hasDrawn",1)}})}function fail(){failFlag=true;$("#done-backtest-pane").removeClass("hidden");$("#backtest-complete").html('<i class="icon icon-remove"></i> 回测失败');$("#inprogress-backtest-pane").addClass("hidden");fillErrorLog(backtestId);enableShare();doneFlag=true;$.each($(".enable-when-done"),function(a,b){$(b).css("color","#333");$(b).css("cursor","pointer")})}var dataResultLog=[];var dataBenchmarkLog=[];var excessResultLog=[];var dataResultBak=[];var dataBenchmarkBak=[];var excessResultBak=[];function changeToLogarithm(){if(chartType=="log"){return}offset=100;if(dataResultLog.length<=0){for(var a=0;a<dataResult.length;a++){dataResultLog[a]={};dataResultLog[a].x=dataResult[a].x;dataResultLog[a].y=dataResult[a].y+offset;dataResultBak[a]={};dataResultBak[a].x=dataResult[a].x;dataResultBak[a].y=dataResult[a].y;dataBenchmarkLog[a]={};dataBenchmarkLog[a].x=dataBenchmark[a].x;dataBenchmarkLog[a].y=dataBenchmark[a].y+offset;dataBenchmarkBak[a]={};dataBenchmarkBak[a].x=dataBenchmark[a].x;dataBenchmarkBak[a].y=dataBenchmark[a].y;excessResultLog[a]={};excessResultLog[a].x=excessResult[a].x;excessResultLog[a].y=(dataResultLog[a].y/dataBenchmarkLog[a].y)*100;excessResultBak[a]={};excessResultBak[a].x=excessResult[a].x;excessResultBak[a].y=excessResult[a].y}}draw(dataResultLog,dataBenchmarkLog,excessResultLog,userRecord,dataGains,dataOrders);chart.yAxis[0].update({type:"logarithmic",labels:{formatter:function(){return(this.value-offset).toFixed(2)+"%"}}},false);for(var a=0;a<3;a++){chart.series[a].update({threshold:offset,tooltip:{pointFormatter:function(){pointFormat='<span style="color:{point.color}">\u25CF</span> {series.name}: <b>'+(this.y-offset).toFixed(2)+"%</b><br/>";return Highcharts.format(pointFormat,{point:this,series:this.series})}}},false)}chart.redraw();chartType="log"}function changeToLine(){if(chartType=="line"){return}draw(dataResultBak,dataBenchmarkBak,excessResultBak,userRecord,dataGains,dataOrders);chart.yAxis[0].update({type:"line",labels:{formatter:function(){return this.value.toFixed(2)+"%"}}},false);for(var a=0;a<3;a++){chart.series[a].update({threshold:0,tooltip:{pointFormatter:function(){pointFormat='<span style="color:{point.color}">\u25CF</span> {series.name}: <b>'+(this.y).toFixed(2)+"%</b><br/>";return Highcharts.format(pointFormat,{point:this,series:this.series})}}},false)}chart.redraw();chartType="line"}$(".chart-type").click(function(){var a=$(this).val();if(a=="log"){changeToLogarithm()}else{changeToLine()}});$("#exceedReturn").click(function(){var a=$(this).is(":checked");if(a){chart.series[2].show()}else{chart.series[2].hide()}});function drawResult(a){stopResult=true;Cy.ajax("/algorithm/backtest/result?backtestId="+a+"&offset="+resultOffset+"&userRecordOffset="+userRecordOffset,{timeout:5000,fail:function(b){stopResult=false;return},error:function(b){stopResult=false;return},success:function(q){if(q.data.state==0){stopResult=false;return}var p=q.data.result.benchmark;var f=q.data.result.overallReturn;var g=q.data.result.gains;var h=q.data.result.orders;var n=q.data.result.count;var k=parseInt(q.data.result.offset);if(n<=0&&q.data.state!=2){if(q.data.state==3){fail()}else{stopResult=false}return}if(!chart){chart=newChart(q.data.userRecord);clearHighchartLable()}if(q.data.userRecord){if(!userRecord){userRecord={};for(var o in q.data.userRecord){userRecord[o]=getRemainNullData()}}for(var o in q.data.userRecord){if(typeof userRecord[o]=="undefined"){userRecord[o]=getRemainNullData();chart.addSeries({name:o,data:userRecord[o],dataGrouping:grouping_options,yAxis:1},false)}}}var d={};var j=null;for(var l=0;l<n;l++){if(!dataResult[l+k]){continue}dataResult[l+k].x=f.time[l];dataResult[l+k].y=f.value[l];excessResult[l+k].x=f.time[l];excessResult[l+k].y=(f.value[l]+100)/(p.value[l]+100)*100-100;dataBenchmark[l+k].x=p.time[l];dataBenchmark[l+k].y=p.value[l];if(dataResult[l+k].y<excessResult[l+k].y){j=dataResult[l+k].y}else{j=excessResult[l+k].y}if(dataBenchmark[l+k].y<j){j=dataBenchmark[l+k].y}if(j<minY){minY=j}dataGains.earn[l+k].x=g.earn.time[l];dataGains.earn[l+k].y=g.earn.value[l];dataGains.lose[l+k].x=g.lose.time[l];dataGains.lose[l+k].y=g.lose.value[l];dataOrders.buy[l+k].x=h.buy.time[l];dataOrders.buy[l+k].y=h.buy.value[l];dataOrders.sell[l+k].x=h.sell.time[l];dataOrders.sell[l+k].y=h.sell.value[l];d[f.time[l]]=l+k}if(q.data.userRecord){var r=100000;for(var o in q.data.userRecord){var e=0;for(var l=0;l<q.data.userRecord[o].time.length;l++){if(!q.data.userRecord[o].time[l]){continue}var t=q.data.userRecord[o].time[l];var s=timeBar[t];if(!userRecord[o][s]){userRecord[o][s]={}}userRecord[o][s].x=q.data.userRecord[o].time[l];userRecord[o][s].y=q.data.userRecord[o].value[l];e++}r=Math.min(r,e)}userRecordOffset=userRecordOffset+r}resultOffset=k+n;if(dataResult.length>0&&resultOffset>0&&dataResult.length>=resultOffset){var m=dataResult[resultOffset-1].x;for(var l=resultOffset;l<dataResult.length;l++){if(dataResult[l].x<m){dataResult[l].x=m;excessResult[l].x=m;dataBenchmark[l].x=m;dataGains.earn[l].x=m;dataGains.lose[l].x=m;dataOrders.buy[l].x=m;dataOrders.sell[l].x=m}else{break}}}draw(dataResult,dataBenchmark,excessResult,userRecord,dataGains,dataOrders);if(q.data.state==3){fail();if(n<=0){doneFlag=true;stopResult=true}return}if(q.data.state==4){failFlag=true;$("#done-backtest-pane").removeClass("hidden");$("#backtest-complete").html('<i class="icon icon-remove"></i> 已取消');$("#inprogress-backtest-pane").addClass("hidden");$.each($(".enable-when-done"),function(c,u){$(u).css("color","#333");$(u).css("cursor","pointer")});doneFlag=true;return}if(q.data.state==2||q.data.state==3){if(n==0){stopCycle=true;$("#detail-finished").html("完成");$("#done-backtest-pane").removeClass("hidden");$("#inprogress-backtest-pane").addClass("hidden");fillStats();doneFlag=true;stopResult=true;$.each($(".enable-when-done"),function(c,u){$(u).css("color","#333");$(u).css("cursor","pointer")});enableLiveTrade();enableShare();isTanChuang();$(".chart-type").removeAttr("disabled");return}}var b=(Math.min(100,(resultOffset/dataResult.length)*100)).toFixed(1);if(b>80){timeoutSpan=1000}$("#backtest-progress-bar").width(b+"%");$("#backtest-progress-label").html(b+"%");stopResult=false}})}Date.prototype.Format=function(a){var c={"M+":this.getMonth()+1,"d+":this.getDate(),"h+":this.getHours(),"m+":this.getMinutes(),"s+":this.getSeconds(),"q+":Math.floor((this.getMonth()+3)/3),S:this.getMilliseconds()};if(/(y+)/.test(a)){a=a.replace(RegExp.$1,(this.getFullYear()+"").substr(4-RegExp.$1.length))}for(var b in c){if(new RegExp("("+b+")").test(a)){a=a.replace(RegExp.$1,(RegExp.$1.length==1)?(c[b]):(("00"+c[b]).substr((""+c[b]).length)))}}return a};var g_tradeDays=null;var timeBar={};function getRemainNullData(){var a=[];for(var b=0;b<g_tradeDays.length;b++){tick=g_tradeDays[b]*1000;a.push({x:tick,y:null});timeBar[tick]=b}return a}function initChartData(){dataResult=getRemainNullData();excessResult=getRemainNullData();dataBenchmark=getRemainNullData();dataOrders.buy=getRemainNullData();dataOrders.sell=getRemainNullData();dataGains.earn=getRemainNullData();dataGains.lose=getRemainNullData();origDataOffset=0;resultOffset=0;userRecordOffset=0;logOffset=0;errorLogOffset=0;if(chart){chart.destroy();userRecord=null;chart=null}}function initChart(a){Cy.ajax("/algorithm/backtest/tradeDays?startDay="+startDate+"&endDay="+endDate,{success:function(b){if(b.data){g_tradeDays=b.data}initChartData();a()},fail:function(b){initChartData();a()}})}function draw(b,d,h,c,a,g){chart.series[0].setData(b,false);chart.series[1].setData(d,false);chart.series[2].setData(h,false);var e=3;if(c){for(var f in c){if(chart.series[e]){chart.series[e].setData(c[f],false)}e++}}chart.series[e++].setData(a.earn,false);chart.series[e++].setData(a.lose,false);chart.series[e++].setData(g.buy,false);chart.series[e].setData(g.sell,false);chart.redraw()}function clearHighchartLable(){$("text[text-anchor=end]").each(function(){if(this.innerHTML=="Highcharts.com"){$(this).html("www.joinquant.com")}})}var hasDrawLeftLine=false;function drawLeftLine(){if(hasDrawLeftLine){return}$("path[stroke=lightgray]").each(function(c){var a=$(this).attr("d").split(" ");if(parseFloat(a[1])<100){for(var b=1;b<a.length;b=b+3){a[b]=10}posNew=a.join(" ");var d=$(this).clone();$(d).attr("d",posNew);$(this.parentNode).append(d)}});hasDrawLeftLine=true}var grouping_options=null;function newChart(a){grouping_options={enabled:!0,approximation:"average",units:[["week",[1]],["month",[1,2,3,4,6]]],groupPixelWidth:1};var c=[{type:"area",name:"策略收益",color:"#4572A7",tooltip:{dateTimeLabelFormats:{day:"%Y-%m-%d,%A"},valueDecimals:2,valueSuffix:"%"},fillOpacity:0.2,id:"returnseries",data:[]},{name:"基准收益",color:"#aa4643",tooltip:{dateTimeLabelFormats:{day:"%Y-%m-%d,%A"},valueDecimals:2,valueSuffix:"%"},data:[]},{name:"超额收益",visible:false,color:"#FFA042",tooltip:{dateTimeLabelFormats:{day:"%Y-%m-%d,%A"},valueDecimals:2,valueSuffix:"%"},data:[]}];var f=null;var e=null;if(a){var b=1;f=16;e=60;for(var d in a){c.push({name:d,data:[],dataGrouping:grouping_options,yAxis:1})}var g=[{height:"36%",lineWidth:2,title:{text:"收益"},tickPixelInterval:20,minorGridLineWidth:1,minorTickWidth:0,opposite:!0,lineWidth:1,plotLines:[{value:0,color:"black",width:2}],labels:{align:"right",x:-3,formatter:function(){return this.value+"%"}}},{labels:{align:"right",x:-3},title:{text:"自定义数据"},tickPixelInterval:20,minorGridLineWidth:1,minorTickWidth:0,opposite:!0,lineWidth:1,plotLines:[{value:0,color:"black",width:2}],top:"40%",height:"20%",offset:0,lineWidth:2}]}else{var b=0;f=26;e=40;var g=[{height:"36%",lineWidth:2,title:{text:"收益"},tickPixelInterval:20,minorGridLineWidth:1,minorTickWidth:0,opposite:!0,lineWidth:1,plotLines:[{value:0,color:"black",width:2}],labels:{align:"right",x:-3,formatter:function(){return this.value+"%"}}}]}g.push({title:{text:"每日盈亏"},plotLines:[{value:0,color:"black",width:2}],top:e+4+"%",height:f+"%",offset:0,lineWidth:2});g.push({title:{text:"每日买卖"},plotLines:[{value:0,color:"black",width:2}],top:e+f+8+"%",height:f+"%",offset:0,lineWidth:2});c.push({type:"column",name:"当日盈利",data:[],dataGrouping:grouping_options,yAxis:b+1});c.push({type:"column",name:"当日亏损",data:[],dataGrouping:grouping_options,tooltip:{dateTimeLabelFormats:{day:"%Y-%m-%d,%A"},pointFormatter:function(h){h='<span style="color:{point.color}">\u25CF</span> {series.name}: <b>'+Math.abs(this.y)+"</b><br/>";return Highcharts.format(h,{point:this,series:this.series})}},yAxis:b+1});c.push({type:"column",name:"当日开仓",data:[],dataGrouping:grouping_options,yAxis:b+2});c.push({type:"column",name:"当日平仓",data:[],dataGrouping:grouping_options,tooltip:{dateTimeLabelFormats:{day:"%Y-%m-%d,%A"},pointFormatter:function(h){h='<span style="color:{point.color}">\u25CF</span> {series.name}: <b>'+Math.abs(this.y)+"</b><br/>";return Highcharts.format(h,{point:this,series:this.series})}},yAxis:b+2});chart=new Highcharts.StockChart({chart:{renderTo:"backtest-chart-outer-container",events:{tooltipRefresh:function(h){chartHoverPointIndex=chart.hoverPoints[0].index}},animation:Highcharts.svg,marginRight:22},exporting:{enabled:false},colors:["#89A54E","#80699B","#18a5ca","#DB843D","#A47D7C"],title:{text:""},rangeSelector:{buttons:[{type:"month",count:1,text:"1个月"},{type:"month",count:12,text:"1年"},{type:"all",text:"全部"}],inputEnabled:true,inputDateFormat:"%Y-%m-%d",selected:4},plotOptions:{series:{turboThreshold:0,connectNulls:true,marker:{states:{hover:{enabled:!0,radius:4}},symbol:"circle"},animation:!1}},legend:{enabled:false,align:"center",verticalAlign:"top",y:55,borderWidth:0},navigator:{series:{color:"transparent",lineWidth:0},height:20,maskFill:"rgba(180, 198, 220, 0.75)",xAxis:{type:"datetime",dateTimeLabelFormats:{day:"%b %e",week:"%b %e",month:"%b %Y"}}},xAxis:{gridLineWidth:1,gridLineColor:"lightgray",categories:[],type:"datetime",tickPixelInterval:120,labels:{style:{fontSize:"10px"},formatter:function(){return Highcharts.dateFormat("%y-%m-%d",this.value)}}},yAxis:g,series:c});return chart}var chartHoverPointIndex=0;document.onkeydown=function(f){var d=chart;var c=d.series[0].points.length;switch(f.keyCode){case 37:if(chartHoverPointIndex==0){chartHoverPointIndex=chartHoverPointIndex}else{chartHoverPointIndex=chartHoverPointIndex-1}var b=[];for(var a=0;a<d.series.length;a++){b[a]=d.series[a].points[chartHoverPointIndex]}d.tooltip.refresh(b);break;case 39:if(chartHoverPointIndex==c){chartHoverPointIndex=chartHoverPointIndex}else{chartHoverPointIndex=chartHoverPointIndex+1}var b=[];for(var a=0;a<d.series.length;a++){b[a]=d.series[a].points[chartHoverPointIndex]}d.tooltip.refresh(b);break}};var transactionTdWidth=null;var transactionDisplayCols=["amount","transaction","type","price","total","gains","commission"];function drawTransactioninfo(c){var j=["日期","时间","品种","标的","交易类型","下单类型","成交数量","成交价","成交额","委托数量","委托价格","平仓盈亏","手续费"];var g=[{name:"date",index:"date",align:"center",sorttype:"date",formatter:"date"},{name:"time",index:"time",align:"center"},{name:"security",index:"security",align:"center"},{name:"stock",index:"stock",align:"center"},{name:"transaction",index:"transaction",align:"center",sorttype:false},{name:"type",index:"type",align:"center",sorttype:false},{name:"amount",index:"amount",align:"center",sorttype:"float"},{name:"price",index:"price",align:"center",sorttype:"float"},{name:"total",index:"total",align:"center",sorttype:"float"},{name:"orderAmount",index:"orderAmount",align:"center",sorttype:"float"},{name:"limitPrice",index:"limitPrice",align:"center",sorttype:"float"},{name:"gains",index:"gains",align:"center",sorttype:"float"},{name:"commission",index:"commission",align:"center",sorttype:"float"}];var b={date:1,time:1,stock:1};var a=$.cookie("default_transaction_cols");if(a&&a.length>0){transactionDisplayCols=a.split(",")}var f={};for(var d=0;d<transactionDisplayCols.length;d++){f[transactionDisplayCols[d]]=1}for(var d=0;d<g.length;d++){if(!f[g[d].index]&&!b[g[d].index]){g[d].hidden=true}}var h=$("#table-transactioninfo").jqGrid({autowidth:true,shrinkToFit:true,data:c,datatype:"local",height:570,rowNum:10000,colNames:j,colModel:g,viewrecords:true,hidegrid:false,altRows:true,grouping:true,groupingView:{groupField:["date"],groupSummary:[true],groupColumnShow:[false],groupText:["<b>{0}</b>"],groupCollapse:false,groupOrder:["asc"]},caption:null});transactionTdWidth=$("#table-transactioninfo").getGridParam("width");var e="";for(var d=0;d<j.length;d++){if(b[g[d].index]){continue}if(!f[g[d].index]){checked=""}else{checked="checked"}e=e+' <div class="checkbox"><label><input type="checkbox" name="transaction-select" value="'+g[d].index+'" '+checked+">"+j[d]+"</label></div>"}$("#transaction-column-select").html(e);return $("#table-transactioninfo")}$("#transaction-column-select").delegate("input","click",function(){var c=$(this).val();if(this.checked){$("#table-transactioninfo").jqGrid("showCol",c);transactionDisplayCols.push(c);var d=transactionDisplayCols.join(",");$.cookie("default_transaction_cols",d)}else{$("#table-transactioninfo").jqGrid("hideCol",c);var a=null;for(var b=0;b<transactionDisplayCols.length;b++){if(transactionDisplayCols[b]==c){a=b;break}}if(a){transactionDisplayCols.splice(a,1)}var d=transactionDisplayCols.join(",");$.cookie("default_transaction_cols",d)}$("#table-transactioninfo").setGridWidth(transactionTdWidth)});var positionTdWidth=null;var positionDisplayCols=["amount","price","position","gain"];function drawPositioninfo(c){var j=["日期","品种","标的","多空","数量","收盘价/结算价","市值/价值","盈亏/逐笔浮盈","开仓均价","持仓均价","保证金","当日盈亏","今手数","仓位占比"];var g=[{name:"date",index:"date",align:"center",sorttype:"date",formatter:"date"},{name:"security",index:"security",align:"center"},{name:"stock",index:"stock",align:"center",sorttype:function(i,k){if(i=='<span class="label label-cash">Cash</span>'){return"*"+i}else{return i}}},{name:"side",index:"side",align:"center"},{name:"amount",index:"amount",align:"center",sorttype:"float"},{name:"price",index:"price",align:"center",sorttype:"float"},{name:"value",index:"value",align:"center",sorttype:"int",formatter:"number",summaryType:"sum",summaryTpl:"<b>总共: {0}</b>"},{name:"gain",index:"gain",align:"center",sorttype:"float"},{name:"avgCost",index:"avgCost",align:"center",sorttype:"float"},{name:"holdCost",index:"holdCost",align:"center",sorttype:"float"},{name:"margin",index:"margin",align:"center",sorttype:"float"},{name:"dailyGains",index:"dailyGains",align:"center",sorttype:"float"},{name:"todayAmount",index:"todayAmount",align:"center",sorttype:"float"},{name:"positionPersent",index:"positionPersent",align:"center",sorttype:"float"}];var b={date:1,time:1,stock:1};var a=$.cookie("default_position_cols");if(a&&a.length>0){positionDisplayCols=a.split(",")}var f={};for(var d=0;d<positionDisplayCols.length;d++){f[positionDisplayCols[d]]=1}for(var d=0;d<g.length;d++){if(!f[g[d].index]&&!b[g[d].index]){g[d].hidden=true}}$("#table-positioninfo").jqGrid({autowidth:true,shrinkToFit:true,data:c,datatype:"local",height:570,rowNum:10000,colNames:j,colModel:g,viewrecords:true,hidegrid:false,altRows:true,grouping:true,groupingView:{groupField:["date"],groupSummary:[true],groupColumnShow:[false],groupText:["<b>{0}</b>"],groupCollapse:false,groupOrder:["asc"]},caption:null});positionTdWidth=$("#table-positioninfo").getGridParam("width");var e="";var h="";for(var d=0;d<j.length;d++){if(b[g[d].index]){continue}if(!f[g[d].index]){h=""}else{h="checked"}e=e+' <div class="checkbox"><label><input type="checkbox" name="position-select" value="'+g[d].index+'" '+h+">"+j[d]+"</label></div>"}$("#position-column-select").html(e);return $("#table-positioninfo")}$("#position-column-select").delegate("input","click",function(){var c=$(this).val();if(this.checked){$("#table-positioninfo").jqGrid("showCol",c);positionDisplayCols.push(c);var d=positionDisplayCols.join(",");$.cookie("default_position_cols",d)}else{$("#table-positioninfo").jqGrid("hideCol",c);var a=null;for(var b=0;b<positionDisplayCols.length;b++){if(positionDisplayCols[b]==c){a=b;break}}if(a){positionDisplayCols.splice(a,1)}var d=positionDisplayCols.join(",");$.cookie("default_position_cols",d)}$("#table-positioninfo").setGridWidth(positionTdWidth)});function drawRisk(c,d,e){if(d.length<=0){return}var b=[{name:"date",index:"date",width:196,align:"center"}];for(var a in d[0]){if(a=="date"){continue}b.push({name:a,index:a,width:175,align:"center",formatter:"currency",formatoptions:{decimalPlaces:4},sorttype:"float"})}$("#"+c).jqGrid({data:d,datatype:"local",height:570,rowNum:10000,colNames:e,colModel:b,viewrecords:true,hidegrid:false,altRows:true})}function drawBenchmarkPeriodReturn(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-benchmark_period_return",a,b);return}function drawAlgorithmPeriodReturn(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-algorithm_period_return",a,b);return}function drawAlpha(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-alpha",a,b);return}function drawBeta(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-beta",a,b);return}function drawSharp(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-sharpe",a,b);return}function drawSortino(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-sortino",a,b);return}function drawInformation(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-information",a,b);return}function drawAlgovolatility(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-algo_volatility",a,b);return}function drawBenchmarkvolatility(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-benchmark_volatility",a,b);return}function drawMaxdrawdown(a){var b=["日期","1个月","3个月","6个月","12个月"];drawRisk("table-max_drawdown",a,b);return}function initTransaction(){addTransaction();if($("#table-transactioninfo").height()<$(".transaction-info-pane").eq(0).height()){setTimeout(initTransaction,5000)}}function fillTransaction(){Cy.ajax("/algorithm/backtest/transactionInfo?backtestId="+backtestId,{success:function(c){$("#transaction-loading").remove();var d=new Array();for(var b=0;b<c.data.transaction.length;b++){d.push(c.data.transaction[b])}var a=drawTransactioninfo(d);transactionOffset=c.data.transaction.length;$("#tab-transactioninfo").find(".ui-jqgrid-bdiv").scroll(function(){nScrollHight=$(this)[0].scrollHeight;nScrollTop=$(this)[0].scrollTop;if(nScrollTop+570>=nScrollHight){addTransaction(nScrollTop)}});bindGroupEvent(a);$("#tab-transactioninfo").attr("_hasDrawn",1);if(c.data.status==1){initTransaction()}}})}var transactionLoading=0;function addTransaction(b){if(transactionLoading==1){return}transactionLoading=1;var a=$("#table-transactioninfo");Cy.ajax("/algorithm/backtest/transactionInfo?backtestId="+backtestId+"&offset="+transactionOffset,{success:function(d){if(d.data.transaction.length<=0){if(d.data.status==1){transactionLoading=0}return}for(var c=0;c<d.data.transaction.length;c++){if(d.data.transaction[c].amount!=0){a.jqGrid("addRowData",null,d.data.transaction[c],"last")}}a.jqGrid("sortGrid","date",true);bindGroupEvent(a);if(b){$("#tab-transactioninfo").find(".ui-jqgrid-bdiv").scrollTop(b)}transactionOffset=transactionOffset+d.data.transaction.length;transactionLoading=0}})}function initPosition(){addPosition();if($("#table-positioninfo").height()<$(".transaction-info-pane").eq(1).height()){setTimeout(initPosition,5000)}}function fillPosition(){Cy.ajax("/algorithm/backtest/positionInfo?backtestId="+backtestId,{success:function(b){$("#position-loading").remove();var a=drawPositioninfo(b.data.position);positionOffset=b.data.position.length;$("#tab-positioninfo").find(".ui-jqgrid-bdiv").scroll(function(){nScrollHight=$(this)[0].scrollHeight;nScrollTop=$(this)[0].scrollTop;if(nScrollTop+570>=nScrollHight){addPosition(nScrollTop)}});a.sortGrid("stock",true,"desc");bindGroupEvent(a);$("#tab-positioninfo").attr("_hasDrawn",1);if(b.data.status==1){initPosition()}}})}var positionLoading=0;function addPosition(b){if(positionLoading==1){return}positionLoading=1;var a=$("#table-positioninfo");Cy.ajax("/algorithm/backtest/positionInfo?backtestId="+backtestId+"&offset="+positionOffset,{success:function(d){if(d.data.position.length<=0){if(d.data.status==1){positionLoading=0}return}for(var c=0;c<d.data.position.length;c++){a.jqGrid("addRowData",null,d.data.position[c],"last")}a.jqGrid("sortGrid","stock",true);bindGroupEvent(a);if(b){$("#tab-positioninfo").find(".ui-jqgrid-bdiv").scrollTop(b)}positionOffset=positionOffset+d.data.position.length;positionLoading=0}})}var riskLength=0;var riskQueryCount=0;function fillRisk(){Cy.ajax("/algorithm/backtest/risk?backtestId="+backtestId,{success:function(a){if(!a.data){setTimeout(fillRisk,2200);return}$(".risk-loading").remove();var b=a.data.risk;if(b==false&&riskLength==0){riskQueryCount++;if(riskQueryCount<=5){setTimeout(fillRisk,2200)}return}riskLength=riskLength+b.algorithmPeriodReturn.length;drawAlgorithmPeriodReturn(b.algorithmPeriodReturn);drawBenchmarkPeriodReturn(b.benchmarkPeriodReturn);drawAlpha(b.alpha);drawBeta(b.beta);drawSharp(b.sharp);drawSortino(b.sortino);drawInformation(b.information);drawAlgovolatility(b.algovolatility);drawBenchmarkvolatility(b.benchmarkvolatility);drawMaxdrawdown(b.maxdrawdown);$(".risk-tab").attr("_hasDrawn",1)}})}function bindGroupEvent(a){a.find(".jqheader").click(function(){var c=this.id;$(this.parentNode.parentNode).jqGrid("groupingToggle",c);return false});a.find(".ui-icon-circlesmall-plus").click(function(){$(this.parentNode.parentNode).trigger("click")});var b=a.attr("id");$(".expand-all-link[tableId="+b+"]").click(function(){var c=$(this).attr("tableId");$("#"+c+" .ui-icon-circlesmall-plus").each(function(){$(this).trigger("click")})});$(".collapse-all-link[tableId="+b+"]").click(function(){var c=$(this).attr("tableId");$("#"+c+" .ui-icon-circlesmall-minus").each(function(){$(this).trigger("click")})})}initChart(function(){timeoutSpan=2000;cycleCheck()});function isTanChuang(){Cy.ajax("/algorithm/backtest/nullBacktestLive",{success:function(a){if(a.code==="00000"){$(".tanceng").removeClass("hidden")}}})}function enableLiveTrade(){if($("#live-trading-link").length==0){if($("#live-trade-btn").attr("_remainCount")>0){$("#live-trade-btn").removeClass("disabled")}}}function enableShare(){if(accessControl!=0){return}$("#share-backtest-button").removeClass("disabled")}$(".x-new").click(function(){$(".tanceng").addClass("hidden")});$(".live-trade-btn").click(function(){if(!$(".tanceng").hasClass("hidden")){$(".tanceng").addClass("hidden")}if($(this).hasClass("disabled")){if($("#live-trading-link").length>0){BootstrapDialog.alert("基于该回测的模拟交易正在进行")}if($("#live-trade-btn").attr("_remainCount")<=0){var c=$("#live-trade-btn").attr("_totalLiveCount");BootstrapDialog.alert("您最多可以同时运行"+c+"个模拟交易")}return}var d=$("#title-box").text();var b=$("#frequency").attr("value");var a=$("#backtestCapital").attr("_cash");Cy.ajax("/algorithm/trade/NewNullTrade",{async:false,success:function(f){if(f.code=="00000"){var g='交易名称： <input id="name" type="text" class="form-control" value="'+d+'-模拟交易" style="width:80%;margin-bottom:10px"><br/>初始资金： <input id="basecapital" type="text" class="form-control" value="'+a+'" style="width:80%;margin-bottom:10px"><br/><div class=""><span style="float:left;margin-right:5px;margin-top:7px">数据频率： </span><select id="frequency" class="form-control live-frequency-select" value="minute"><option value="day" class="live-frequency-option">每天</option><option value="minute" class="live-frequency-option">分钟</option><option value="tick" class="live-frequency-option">TICK</option></select></div><br/>开始日期： <input type="text"  name="startTime" class="form-control" style="width:80%;margin-bottom:10px;background-color:white" id="startTime"  readonly="readonly"><br/>';if(f.data.length>0){g+='<span style="float:left;margin-right:5px;margin-top:7px;width:100px">时限： </span><br/><select id="expireTime" class="form-control live-frequency-select" value="minute">';for(var e=0;e<f.data.length;e++){if(f.data[e].expireTime=="2030-12-31 00:00:00"){g+='<option value="'+f.data[e].expireTime+'">永久</option>'}else{g+='<option value="'+f.data[e].expireTime+'">限时 ('+f.data[e].expireTime.substring(0,10)+"到期)</option>"}}g+="</select>";BootstrapDialog.show({title:"新建模拟交易",message:g,onshown:function(k){k.getModalBody().find("#frequency").val(b);var l=k.getModalBody().find("#startTime");var m=new Date();var i=m.getFullYear()+"-"+(m.getMonth()+1)+"-"+m.getDate();m.setDate(m.getDate()+1);var h=m.getFullYear()+"-"+(m.getMonth()+1)+"-"+(m.getDate());var j=l.datepicker({dateFormat:"yy-mm-dd",minDate:liveMinDate,changeYear:true,changeMonth:true,beforeShow:function(){setTimeout(function(){$("#ui-datepicker-div").css("z-index",100007)},100)},onSelect:function(o,n){}});k.getModalBody().find("#startTime").val(h)},buttons:[{label:"提交",action:function(n){var o=n.getModalBody().find("#basecapital").val();var j=n.getModalBody().find("#name").val();var l=n.getModalBody().find("#frequency").val();var k=n.getModalBody().find("#startTime").val();var h=n.getModalBody().find("#expireTime").val();if(h==false){alert("请选择时限");return false}o=$.trim(o);var p=/^\d+(\.\d+)?$/;var i=p.test(o);if(!i){alert("请输入一个正整数!");return false}var m=$("input[id=backtestId]").val();Cy.ajax("/algorithm/live/submit",{data:"backtestId="+m+"&basecapital="+o+"&name="+encodeURIComponent(j)+"&frequency="+l+"&startTime="+k+"&expireTime="+h,async:false,success:function(q){window.location.href="/algorithm/live/index?backtestId="+q.data.backtestId;return false},fail:function(q){BootstrapDialog.show({title:"提示",btnOKLabel:"确认",message:q.msg})}})}},{label:"取消",action:function(h){h.close()}}]})}else{BootstrapDialog.show({title:"提示",btnOKLabel:"确认",message:"模拟交易位不足"})}}}})});$(".icon-edit").click(function(b){var c=$(this.parentNode).find("#title-box").eq(0).text();var a=$(this).attr("_backtestId");var d=this;BootstrapDialog.show({title:"修改回测名称",message:'名称： <input id="name" type="text" class="form-control" value="'+c+'" style="width:80%;margin-bottom:10px"><br/></div>',buttons:[{label:"提交",action:function(e){if(e.getModalBody().find("#name").val()){var f=e.getModalBody().find("#name").val()}else{var f=$("#title-box").text()}Cy.ajax("/algorithm/backtest/setName",{data:"backtestId="+a+"&name="+f,async:false,success:function(g){$(d.parentNode).find("#title-box").eq(0).text(f);e.close();return false},fail:function(g){e.close();BootstrapDialog.show({title:"提示",btnOKLabel:"确认",message:g.msg})}})}},{label:"取消",action:function(e){e.close()}}]});b.stopPropagation();return false});function getByteLen(e){var b=0;for(var d=0;d<e.length;d++){var c=e.charAt(d);if(c.match(/[^\x00-\xff]/ig)!=null){b+=15}else{b+=7}}return b}function Left(){var a=getByteLen($("#title-box").text());if($("#title-box").width()>=a){$(".icon-edit").css({left:a+14})}else{$(".icon-edit").css({left:"calc(100% - 248px)"})}}if($("body").hasClass("mobile")){Left()}var evt="onorientationchange" in window?"orientationchange":"resize";window.addEventListener(evt,function(){Left()},false);function mobile(){var b=$(".dailybars-output").height();$(".after").height(b);$("#backtest-menu-more").click(function(){b=$(".dailybars-output").height();$(".after").height(b);if($("#result-area").css("display")=="block"){$("#result-area").css({display:"none"})}else{$("#result-area").css({display:"block"})}});$("#result-tabs").click(function(){$(this).parent().css({display:"none"})}).next(".after").click(function(){$(this).parent().css({display:"none"})});var a=$(window).width();$(".dailybars-output").width(a).css({overflow:"auto"})}if($("body").hasClass("mobile")){mobile()};