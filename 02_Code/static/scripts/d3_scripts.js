    function pieChardFunction()
    {
            var data = dataFound;
            var barValueToCheck = keyForGraph;
            var labelGraph = labelForGraph;
            var valueLabelWidth = 100; // space reserved for value labels (right)
            var barHeight = 20; // height of one bar
            var barLabelWidth = 300; // space reserved for bar labels
            var barLabelPadding = 5; // padding between bar and bar labels (left)
            var gridLabelHeight = 18; // space reserved for gridline labels
            var gridChartOffset = 3; // space between start of grid and first bar
            var maxBarWidth = 420; // width of the bar with the max value

            // Accessor functions
            var barLabel = function (d) { return d[labelGraph]; };
            var barValue = function (d) { return parseFloat(d[barValueToCheck]); };

            // Scales
            var yScale = d3.scale.ordinal().domain(d3.range(0, data.length)).rangeBands([0, data.length * barHeight]);
            var y = function (d, i) { return yScale(i); };
            var yText = function (d, i) { return y(d, i) + yScale.rangeBand() / 2; };
            var x = d3.scale.linear().domain([0, d3.max(data, barValue)]).range([0, maxBarWidth]);

            // Svg container element
            var chart = d3.select('#myresult').append("svg")
           .attr('width', maxBarWidth + barLabelWidth + valueLabelWidth)
           .attr('height', gridLabelHeight + gridChartOffset + data.length * barHeight);

            // Grid line labels
            var gridContainer = chart.append('g')
            .attr('transform', 'translate(' + barLabelWidth + ',' + gridLabelHeight + ')');
            gridContainer.selectAll("text").data(x.ticks(10)).enter().append("text")
           .attr("x", x)
           .attr("dy", -3)
           .attr("text-anchor", "middle")
           .text(String);

            // Vertical grid lines
            gridContainer.selectAll("line").data(x.ticks(10)).enter().append("line")
           .attr("x1", x)
           .attr("x2", x)
           .attr("y1", 0)
           .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
           .style("stroke", "#ccc");

            // Bar labels
            var labelsContainer = chart.append('g')
           .attr('transform', 'translate(' + (barLabelWidth - barLabelPadding) + ',' + (gridLabelHeight + gridChartOffset) + ')');
            labelsContainer.selectAll('text').data(data).enter().append('text')
           .attr('y', yText)
           .attr('stroke', 'none')
           .attr('fill', 'black')
           .attr("dy", ".35em")

            // Vertical-align: middle
           .attr('text-anchor', 'end')
           .text(barLabel);

            // Bars
            var barsContainer = chart.append('g')
            .attr('transform', 'translate(' + barLabelWidth + ',' + (gridLabelHeight + gridChartOffset) + ')');
            barsContainer.selectAll("rect").data(data).enter().append("rect")
           .attr('y', y)
           .attr('height', yScale.rangeBand())
           .attr('width', function (d) { return x(barValue(d)); })
           .attr('stroke', 'Gray')
           .attr('fill', '#5eb9d7');

            // Bar value labels
            barsContainer.selectAll("text").data(data).enter().append("text")
           .attr("x", function (d) { return x(barValue(d)); })
           .attr("y", yText)
           .attr("dx", 3)
           .attr("dy", ".35em")
           .attr("text-anchor", "start")
           .attr("fill", "black")
           .attr("stroke", "none")
           .text(function (d) { return d3.round(barValue(d), 2); });

            // Start line
            barsContainer.append("line")
           .attr("y1", -gridChartOffset)
           .attr("y2", yScale.rangeExtent()[1] + gridChartOffset)
           .style("stroke", "#000");
        }

        // Function to creat dynamic Tables.
// data: data as Json
// columns: columns which should be used in format: ['column1', 'column2']
function tabulate(data, columns) {
		var table = d3.select('#myResultTable').append('table')
                    .style('table-layout', 'auto');
		var thead = table.append('thead')
		var	tbody = table.append('tbody');

		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(data)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}


