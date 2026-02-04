<template>
  <div class="module daily-activity-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Dagelijkse activiteit</h2>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as d3 from 'd3'
import { getPostsPerDay } from '../database'

const chartContainer = ref(null)

onMounted(async () => {
  const { data, error } = await getPostsPerDay(20)
  if (error) {
    console.error('Failed to fetch daily activity:', error)
    return
  }

  // Chart dimensions - responsive to container
  const margin = { top: 10, right: 10, bottom: 30, left: 40 }
  const containerWidth = chartContainer.value.offsetWidth
  const width = containerWidth - margin.left - margin.right
  const height = 250 - margin.top - margin.bottom

  // Create SVG
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // X scale
  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, width])
    .padding(0.2)

  // Y scale
  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count)])
    .range([height, 0])

  // X axis - minimalist style
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x)
      .tickFormat((d, i) => {
        // Only show every 5th date
        if (i % 5 === 0) {
          const parts = d.split('-')
          return `${parts[2]}/${parts[1]}`
        }
        return ''
      })
      .tickSize(0))
    .select('.domain')
    .attr('stroke', '#E5E7EB') // Light gray

  // Style x-axis text
  svg.selectAll('.tick text')
    .attr('fill', '#6B7280')
    .style('font-size', '11px')

  // Y axis - minimalist style
  svg.append('g')
    .call(d3.axisLeft(y)
      .ticks(5)
      .tickSize(0)
      .tickPadding(8))
    .select('.domain')
    .attr('stroke', '#E5E7EB') // Light gray

  // Style y-axis text
  svg.selectAll('.tick text')
    .attr('fill', '#6B7280')
    .style('font-size', '11px')

  // Add horizontal grid lines
  svg.selectAll('.grid-line')
    .data(y.ticks(5))
    .enter()
    .append('line')
    .attr('class', 'grid-line')
    .attr('x1', 0)
    .attr('x2', width)
    .attr('y1', d => y(d))
    .attr('y2', d => y(d))
    .attr('stroke', '#F3F4F6')
    .attr('stroke-width', 1)

  // Add bars
  svg.selectAll('.bar')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.date))
    .attr('y', d => y(d.count))
    .attr('width', x.bandwidth())
    .attr('height', d => height - y(d.count))
    .attr('fill', '#8A89C0') // lavender color
    .attr('rx', 2) // Slightly rounded corners
    .on('mouseover', function(event, d) {
      d3.select(this)
        .attr('fill', '#B084CC') // amethyst on hover
    })
    .on('mouseout', function(event, d) {
      d3.select(this)
        .attr('fill', '#8A89C0') // back to lavender
    })
})
</script>

<style scoped>
.chart-container {
  overflow-x: auto;
}
</style>
