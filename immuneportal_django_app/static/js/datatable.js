var this_js_script = $('script[src*=datatable]');


var my_var_1 = this_js_script.attr('data-my_var_1');   

console.log('injs');
console.log(my_var_1); 

var data_file = "http://localhost:8000"+$('#urlVal').val(); 
$(document).ready(function() {
	$.ajax({
	    url: data_file,
	    method: 'GET',
	    //datatype: 'json',
	    
	    
       	    //console.log(data_file);
            //console.log(data_file);
	    success: function (data) {
	//console.log('hello');
	//console.log(data_file);
	    console.log(data);
	    $.fn.dataTable.ext.errMode = 'throw';
	    $('#resultTable').DataTable( {
		    "processing": true,
		"scrollX": true,
		"data":JSON.parse(data).data,
		"columns": [
			/*{ data: "chr" },
            		{ data: "pos" },
            		{ data: "ref" },
            		{ data: "alt" },
            		{ data: "disease prob" },
            		{ data: "FDR"},
		    { data: "transcript"},
		    { data: "ON/OFF splicing site"},
		    { data: "upstream intron length" },
		    { data: "exon length" },
		    { data: "downstream intron length" },
		    { data: "proximity acceptor site"},
		    { data: "proximity donor site"},
		    { data: "conservation"},
		    { data: "acceptor_site strength"},
		    { data: "donor_site strength"},
		    { data: "junction score change"},
		    { data: "PTM"},
		    { data: "Pfam"}*/
		    { "data": "chr" },
		    { "data": "pos" },
		    { "data": "ref" },
		    { "data": "alt" },
		    { "data": "disease prob" },
		    { "data": "FDR"},
		    { "data": "transcript"},
		    { "data": "ON/OFF splicing site"},
		    { "data": "upstream intron length" },
		    { "data": "exon length" },
		    { "data": "downstream intron length" },
		    { "data": "proximity acceptor site"},
		    { "data": "proximity donor site"},
		    { "data": "conservation"},
		    { "data": "acceptor_site strength"},
		    { "data": "donor_site strength"},
		    { "data": "junction score change"},
		    { "data": "PTM"},
		    { "data": "Pfam"}
		]
	    } );
	    var table = $('#resultTable').DataTable();
	    }
	});
	$('#resultTable tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('info') ) {
            $(this).removeClass('info');
        }
        else {
            table.$('tr.info').removeClass('info');
            $(this).addClass('info');
		}
		var record = table.row(this).data();
        console.log(record['chr'].substring(3));
        browser.setLocation(record['chr'].substring(3), parseInt(record['pos']) - 50, parseInt(record['pos']) + 50);
    } );
    var browser =  new Browser({
      chr:          '22',
      viewStart:    30700000,
      viewEnd:      30900000,

      coordSystem: {
        speciesName: 'Human',
        taxon: 9606,
        auth: 'GRCh',
        version: '37',
        ucscName: 'hg19'
      },

      sources:     [{name:                 'Genome',
                     twoBitURI:            '//www.biodalliance.org/datasets/hg19.2bit',
                     tier_type:            'sequence'},
                    {name:                 'Genes',
                     desc:                 'Gene structures from GENCODE 19',
                     bwgURI:               '//www.biodalliance.org/datasets/gencode.bb',
                     stylesheet_uri:       '//www.biodalliance.org/stylesheets/gencode.xml',
                     collapseSuperGroups:  true,
                     trixURI:              '//www.biodalliance.org/datasets/geneIndex.ix'},
                    {name:                 'Repeats',
                     desc:                 'Repeat annotation from Ensembl',
                     bwgURI:               '//www.biodalliance.org/datasets/repeats.bb',
                     stylesheet_uri:       '//www.biodalliance.org/stylesheets/bb-repeats.xml'},
                    {name:                 'Conservation',
                     desc:                 'Conservation', 
                     bwgURI:               'app/regsnp-intron/annotation/hg19.100way.phyloP100way.bw',
                     noDownsample:         true}],

    });
	
    
} );



