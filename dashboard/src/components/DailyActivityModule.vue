<template>
  <div class="module daily-activity-module bg-white border border-1 border-amethyst-200 p-4 md:p-8 w-full">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Dagelijkse activiteit</h2>
    <p class="text-sm mb-4 text-gray-400">Het aantal posts per dag met misinformatie.</p>
    <div ref="chartContainer" class="chart-container relative"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as d3 from 'd3'
import { getPostsPerDay } from '../database'

const chartContainer = ref(null)
const router = useRouter()

onMounted(async () => {
  const { data, error } = await getPostsPerDay(20)
  if (error) {
    console.error('Failed to fetch daily activity:', error)
    return
  }

  const margin = { top: 10, right: 10, bottom: 30, left: 40 }
  const containerWidth = chartContainer.value.offsetWidth
  const width = containerWidth - margin.left - margin.right
  const height = 250 - margin.top - margin.bottom

  const tooltip = document.createElement('div')
  Object.assign(tooltip.style, {
    position: 'absolute',
    background: 'rgba(0,0,0,0.72)',
    color: 'white',
    fontSize: '12px',
    padding: '3px 8px',
    borderRadius: '4px',
    pointerEvents: 'none',
    whiteSpace: 'nowrap',
    opacity: '0',
    transition: 'opacity 0.1s',
    transform: 'translate(-50%, -100%)',
  })
  chartContainer.value.appendChild(tooltip)

  const supportsHover = window.matchMedia('(hover: hover)').matches

  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, width])
    .padding(0.2)

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count)])
    .range([height, 0])

  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x)
      .tickFormat((d, i) => {
        if (i % 5 === 0) {
          const parts = d.split('-')
          return `${parts[2]}/${parts[1]}`
        }
        return ''
      })
      .tickSize(0))
    .select('.domain')
    .attr('stroke', '#E5E7EB')

  svg.selectAll('.tick text')
    .attr('fill', '#6B7280')
    .style('font-size', '11px')

  svg.append('g')
    .call(d3.axisLeft(y)
      .ticks(5)
      .tickSize(0)
      .tickPadding(8))
    .select('.domain')
    .attr('stroke', '#E5E7EB')

  svg.selectAll('.tick text')
    .attr('fill', '#6B7280')
    .style('font-size', '11px')

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

  svg.selectAll('.bar')
    .data(data)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.date))
    .attr('y', d => y(d.count))
    .attr('width', x.bandwidth())
    .attr('height', d => height - y(d.count))
    .attr('fill', '#8A89C0')
    .attr('rx', 2)
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this).attr('fill', '#B084CC')
      if (!supportsHover) return
      const barTop = margin.top + y(d.count)
      const fitsAbove = barTop > 32
      tooltip.textContent = `${d.count} posts`
      tooltip.style.left = `${margin.left + x(d.date) + x.bandwidth() / 2}px`
      tooltip.style.top = fitsAbove ? `${barTop - 6}px` : `${barTop + 6}px`
      tooltip.style.transform = fitsAbove ? 'translate(-50%, -100%)' : 'translate(-50%, 0)'
      tooltip.style.opacity = '1'
    })
    .on('mouseout', function(event, d) {
      d3.select(this).attr('fill', '#8A89C0')
      tooltip.style.opacity = '0'
    })
    .on('click', function(event, d) {
      router.push({ path: '/posts', query: { startDate: d.date, endDate: d.date } })
    })
})
</script>

<style scoped>
.chart-container {
  overflow-x: auto;
}
</style>
