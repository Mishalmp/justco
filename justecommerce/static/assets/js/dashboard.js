(function($) {
	document.querySelector('#bannerClose').addEventListener('click',function() {
		document.querySelector('#proBanner').classList.add('d-none');
	});
	'use strict';
	$(function() {
		if ($(".dashboard-progress-1").length) {
			$('.dashboard-progress-1').circleProgress({
				value: 0.70,
				size: 125,
				thickness: 7,
				startAngle: 80,
				fill: {
					gradient: ["#7922e5", "#1579ff"]
				}
			});
		}
		if ($(".dashboard-progress-1-dark").length) {
			$('.dashboard-progress-1-dark').circleProgress({
				value: 0.70,
				size: 125,
				thickness: 7,
				startAngle: 10,
				emptyFill: '#eef0fa',
				fill: {
					gradient: ["#7922e5", "#1579ff"]
				}
			});
		}

		if ($(".dashboard-progress-2").length) {
			$('.dashboard-progress-2').circleProgress({
				value: 0.60,
				size: 125,
				thickness: 7,
				startAngle: 10,
				fill: {
					gradient: ["#429321", "#b4ec51"]
				}
			});
		}
		if ($(".dashboard-progress-2-dark").length) {
			$('.dashboard-progress-2-dark').circleProgress({
				value: 0.60,
				size: 125,
				thickness: 7,
				startAngle: 10,
				emptyFill: '#eef0fa',
				fill: {
					gradient: ["#429321", "#b4ec51"]
				}
			});
		}

		if ($(".dashboard-progress-3").length) {
			$('.dashboard-progress-3').circleProgress({
				value: 0.90,
				size: 125,
				thickness: 7,
				startAngle: 10,
				fill: {
					gradient: ["#f76b1c", "#fad961"]
				}
			});
		}
		if ($(".dashboard-progress-3-dark").length) {
			$('.dashboard-progress-3-dark').circleProgress({
				value: 0.90,
				size: 125,
				thickness: 7,
				startAngle: 10,
				emptyFill: '#eef0fa',
				fill: {
					gradient: ["#f76b1c", "#fad961"]
				}
			});
		}

		if ($(".dashboard-progress-4").length) {
			$('.dashboard-progress-4').circleProgress({
				value: 0.45,
				size: 125,
				thickness: 7,
				startAngle: 10,
				fill: {
					gradient: ["#9f041b", "#f5515f"]
				}
			});
		}
		if ($(".dashboard-progress-4-dark").length) {
			$('.dashboard-progress-4-dark').circleProgress({
				value: 0.45,
				size: 125,
				thickness: 7,
				startAngle: 10,
				emptyFill: '#eef0fa',
				fill: {
					gradient: ["#9f041b", "#f5515f"]
				}
			});
    }
    
		if ($("#total-profit").length) {
			var totalProfitData = {
				labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
				datasets: [{
					label: 'Margin',
					data: [5, 4, 6, 4.5, 5.5, 4, 5, 4.2, 5.5],
					backgroundColor: [
						'#cfe1ff',
					],
					borderColor: [
						'#0062ff'
					],
					borderWidth: 3,
					fill: true,
				}],
			};
			var totalProfitOptions = {
				scales: {
					yAxes: [{
						display: false,
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
					xAxes: [{
						display: false,
						position: 'bottom',
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
				},
				legend: {
					display: false,
				},
				elements: {
					point: {
						radius: 0
					},
					line: {
						tension: 0
					}
				},
				tooltips: {
					backgroundColor: 'rgba(2, 171, 254, 1)',
				},
			};
			var barChartCanvas = $("#total-profit").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'line',
				data: totalProfitData,
				options: totalProfitOptions,
			});
    }
    
		if ($("#total-profit-dark").length) {
			var graphGradient = document.getElementById("total-profit-dark").getContext('2d');;
			var saleGradientBg = graphGradient.createLinearGradient(15, 0, 15, 190);
			saleGradientBg.addColorStop(0, 'rgba(0, 98, 255, .3)');
			saleGradientBg.addColorStop(1, 'rgba(0, 0, 0, .2)');
			var totalProfitDarkData = {
				labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
				datasets: [{
					label: 'Margin',
					data: [5, 4, 6, 4.5, 5.5, 4, 5, 4.2, 5.5],
					backgroundColor: saleGradientBg,
					borderColor: [
						'#0062ff'
					],
					borderWidth: 3,
					fill: true,
				}],
			};
			var totalProfitDarkOptions = {
				scales: {
					yAxes: [{
						display: false,
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10,
						}
					}],
					xAxes: [{
						display: false,
						position: 'bottom',
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10,
						}
					}],
				},
				legend: {
					display: false,
				},
				elements: {
					point: {
						radius: 0
					},
					line: {
						tension: 0
					}
				},
				tooltips: {
					backgroundColor: 'rgba(2, 171, 254, 1)',
				},
			};
			var barChartCanvas = $("#total-profit-dark").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'line',
				data: totalProfitDarkData,
				options: totalProfitDarkOptions,
			});
		}

		if ($("#total-expences").length) {
			var totalExpencesData = {
				labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
				datasets: [{
					label: 'Margin',
					data: [4, 5, 6, 5, 4, 5, 4, 6, 5],
					backgroundColor: [
						'#e1fff3',
					],
					borderColor: [
						'#3dd597'
					],
					borderWidth: 3,
					fill: true,
				}],
			};
			var totalExpencesOptions = {
				scales: {
					yAxes: [{
						display: false,
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
					xAxes: [{
						display: false,
						position: 'bottom',
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
				},
				legend: {
					display: false,
				},
				elements: {
					point: {
						radius: 0
					},
					line: {
						tension: 0
					}
				},
				tooltips: {
					backgroundColor: 'rgba(2, 171, 254, 1)',
				},
			};
			var barChartCanvas = $("#total-expences").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'line',
				data: totalExpencesData,
				options: totalExpencesOptions,
			});
    }
    
		if ($("#total-expences-dark").length) {
			var graphGradient = document.getElementById("total-expences-dark").getContext('2d');;
			var saleGradientBg = graphGradient.createLinearGradient(15, 0, 15, 190);
			saleGradientBg.addColorStop(0, 'rgba(61, 213, 151, .3)');
			saleGradientBg.addColorStop(1, 'rgba(0, 0, 0, .2)');
			var totalExpencesDarkData = {
				labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
				datasets: [{
					label: 'Margin',
					data: [4, 5, 6, 5, 4, 5, 4, 6, 5],
					backgroundColor: saleGradientBg,
					borderColor: [
						'#3dd597'
					],
					borderWidth: 3,
					fill: true,
				}],
			};
			var totalExpencesDarkOptions = {
				scales: {
					yAxes: [{
						display: false,
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
					xAxes: [{
						display: false,
						position: 'bottom',
						gridLines: {
							drawBorder: false,
							display: false,
							drawTicks: false
						},
						ticks: {
							beginAtZero: true,
							stepSize: 10
						}
					}],
				},
				legend: {
					display: false,
				},
				elements: {
					point: {
						radius: 0
					},
					line: {
						tension: 0
					}
				},
				tooltips: {
					backgroundColor: 'rgba(2, 171, 254, 1)',
				},
			};
			var barChartCanvas = $("#total-expences-dark").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'line',
				data: totalExpencesDarkData,
				options: totalExpencesDarkOptions,
			});
		}

		if ($("#devices-sales").length) {
			var deviceSalesData = {
				labels: ["Hublot", "Rolex", "Chopard", "Apple", "Fossil", "Cartier",'Casio','Fossil'],
				datasets: [{
						label: 'Demand',
						data: [450, 500, 300, 350, 200, 320, 310, 700],
						backgroundColor: [
							'#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8',
						],
						borderColor: [
							'#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8', '#a461d8',
						],
						borderWidth: 1,
						fill: false
					},
					{
						label: 'Supply',
						data: [250, 100, 310, 75, 290, 100, 500, 260],
						backgroundColor: [
							'#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a',
						],
						borderColor: [
							'#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a', '#fc5a5a',
						],
						borderWidth: 1,
						fill: false
					}
				]
			};
			var deviceSalesOptions = {
				scales: {
					xAxes: [{
						stacked: false,
						barPercentage: .5,
						categoryPercentage: 0.4,
						position: 'bottom',
						display: true,
						gridLines: {
							display: false,
							drawBorder: false,
							drawTicks: false
						},
						ticks: {
							display: true, //this will remove only the label
							stepSize: 500,
							fontColor: "#a7afb7",
							fontSize: 14,
							padding: 10,
						}
					}],
					yAxes: [{
						stacked: false,
						display: true,
						gridLines: {
							drawBorder: false,
							display: true,
							color: "#eef0fa",
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							display: true,
							beginAtZero: true,
							stepSize: 200,
							fontColor: "#a7afb7",
							fontSize: 14,
							callback: function(value, index, values) {
								return value + 'k';
							},
						},
					}]
				},
				legend: {
					display: false
				},
				legendCallback: function(chart) {
					var text = [];
					text.push('<ul class="' + chart.id + '-legend">');
					for (var i = 0; i < chart.data.datasets.length; i++) {
						text.push('<li><span class="legend-box" style="background:' + chart.data.datasets[i].backgroundColor[i] + ';"></span><span class="legend-label text-dark">');
						if (chart.data.datasets[i].label) {
							text.push(chart.data.datasets[i].label);
						}
						text.push('</span></li>');
					}
					text.push('</ul>');
					return text.join("");
				},
				tooltips: {
					backgroundColor: 'rgba(0, 0, 0, 1)',
				},
				plugins: {
					datalabels: {
						display: false,
						align: 'center',
						anchor: 'center'
					}
				}
			};
			var barChartCanvas = $("#devices-sales").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: deviceSalesData,
				options: deviceSalesOptions
			});
			document.getElementById('devices-sales-legend').innerHTML = barChart.generateLegend();
    }
    


		if ($("#account-retension").length) {
			var accountRetensionData = {
				labels: ["Jan", "Feb", "Mar", "Apr", "May"],
				datasets: [{
						label: 'Demand',
						data: [33, 48, 39, 36, 36],
						backgroundColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderWidth: 1,
						fill: false
					},
					{
						label: 'Demand',
						data: [94, 28, 49, 25, 20],
						backgroundColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderWidth: 1,
						fill: false
					},
					{
						label: 'Demand',
						data: [66, 33, 25, 36, 69],
						backgroundColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderColor: [
							'#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8', '#d8d8d8',
						],
						borderWidth: 1,
						fill: false
					}
				]
			};
			var accountRetensionOptions = {
				scales: {
					xAxes: [{
						stacked: false,
						position: 'bottom',
						display: true,
						barPercentage: .7,
						categoryPercentage: 1,
						gridLines: {
							display: false,
							drawBorder: false,
							drawTicks: false
						},
						ticks: {
							display: true, //this will remove only the label
							stepSize: 500,
							fontColor: "#a7afb7",
							fontSize: 14,
							padding: 10,
						}
					}],
					yAxes: [{
						stacked: false,
						display: true,
						gridLines: {
							drawBorder: false,
							display: true,
							color: "#c31a56",
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							display: false,
							beginAtZero: true,
							stepSize: 40,
							fontColor: "#a7afb7",
							fontSize: 14,
							callback: function(value, index, values) {
								return value + 'k';
							},

						},
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					backgroundColor: 'rgba(0, 0, 0, 1)',
				},
				plugins: {
					datalabels: {
						display: false,
						align: 'center',
						anchor: 'center'
					}
				}
			};
			var barChartCanvas = $("#account-retension").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: accountRetensionData,
				options: accountRetensionOptions
			});
		}

		
		
		
		if ($("#my-balance").length) {
			var myBalanceData = {
				labels: ["Jan", "Feb", "Mar", "Apr"],
				datasets: [{
						label: 'Demand',
						data: [90, 85, 100, 105],
						backgroundColor: [
							'#0062ff', '#0062ff', '#0062ff', '#0062ff',
						],
						borderColor: [
							'#0062ff', '#0062ff', '#0062ff', '#0062ff',
						],
						borderWidth: 1,
						fill: false
					},
					{
						label: 'Supply',
						data: [200, 200, 200, 200],
						backgroundColor: [
							'#eef0fa', '#eef0fa', '#eef0fa', '#eef0fa',
						],
						borderColor: [
							'#eef0fa', '#eef0fa', '#eef0fa', '#eef0fa',
						],
						borderWidth: 1,
						fill: false
					}
				]
			};
			var myBalanceOptions = {
				scales: {
					xAxes: [{
						stacked: true,
						barPercentage: .7,
						position: 'bottom',
						display: true,
						gridLines: {
							display: false,
							drawBorder: false,
							drawTicks: false
						},
						ticks: {
							display: true, //this will remove only the label
							stepSize: 500,
							fontColor: "#111",
							fontSize: 12,
							padding: 10,
						}
					}],
					yAxes: [{
						stacked: false,
						display: false,
						gridLines: {
							drawBorder: true,
							display: false,
							color: "#eef0fa",
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							display: true,
							beginAtZero: true,
							stepSize: 200,
							fontColor: "#a7afb7",
							fontSize: 14,
							callback: function(value, index, values) {
								return value + 'k';
							},

						},
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					backgroundColor: 'rgba(0, 0, 0, 1)',
				},
				plugins: {
					datalabels: {
						display: false,
						align: 'center',
						anchor: 'center'
					}
				}
			};
			var barChartCanvas = $("#my-balance").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: myBalanceData,
				options: myBalanceOptions
			});
    }
    
		if ($("#my-balance-dark").length) {
			var myBalanceDarkData = {
				labels: ["Jan", "Feb", "Mar", "Apr"],
				datasets: [{
						label: 'Demand',
						data: [90, 85, 100, 105],
						backgroundColor: [
							'#0062ff', '#0062ff', '#0062ff', '#0062ff',
						],
						borderColor: [
							'#0062ff', '#0062ff', '#0062ff', '#0062ff',
						],
						borderWidth: 1,
						fill: false
					},
					{
						label: 'Supply',
						data: [200, 200, 200, 200],
						backgroundColor: [
							'#2b2b36', '#2b2b36', '#2b2b36', '#2b2b36',
						],
						borderColor: [
							'#2b2b36', '#2b2b36', '#2b2b36', '#2b2b36',
						],
						borderWidth: 1,
						fill: false
					}
				]
			};
			var myBalanceDarkOptions = {
				scales: {
					xAxes: [{
						stacked: true,
						barPercentage: .7,
						position: 'bottom',
						display: true,
						gridLines: {
							display: false,
							drawBorder: false,
							drawTicks: false
						},
						ticks: {
							display: true, //this will remove only the label
							stepSize: 500,
							fontColor: "#fff",
							fontSize: 12,
							padding: 10,
						}
					}],
					yAxes: [{
						stacked: false,
						display: false,
						gridLines: {
							drawBorder: true,
							display: false,
							color: "#eef0fa",
							drawTicks: false,
							zeroLineColor: 'rgba(90, 113, 208, 0)',
						},
						ticks: {
							display: true,
							beginAtZero: true,
							stepSize: 200,
							fontColor: "#a7afb7",
							fontSize: 14,
							callback: function(value, index, values) {
								return value + 'k';
							},

						},
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					backgroundColor: 'rgba(0, 0, 0, 1)',
				},
				plugins: {
					datalabels: {
						display: false,
						align: 'center',
						anchor: 'center'
					}
				}
			};
			var barChartCanvas = $("#my-balance-dark").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: myBalanceDarkData,
				options: myBalanceDarkOptions
			});
		}

		
    
	
	
    
		
	
    
	
    
	});
})(jQuery);