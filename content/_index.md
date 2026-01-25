---
# Leave the homepage title empty to use the site title
title: "Adin's Portfolio"
date: 2022-10-24
type: landing

outputs: [HTML, RSS]

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: uploads/resume.pdf
    design:
      css_class: dark
      css_style: "margin-top: 0rem; margin-bottom: 6rem; padding-bottom: 12rem; padding-top: 0rem;"
      background:
        color: black
        image:
          # Add your image background to `assets/media/`.
          filename: signal_background.svg
          filters:
            brightness: 1.0
          size: cover
          position: center
          parallax: false

  - block: collection
    id: sel_projects
    content:
      title: Selected Projects
      filters:
        folders:
          - project
        featured_only: true
    design:
      view: article-grid
      columns: 2

  - block: markdown
    content:
      title: 'My Interests'
      subtitle: ''
      text: |-
        I’m interested in performance-critical systems for modern ML—especially attention and sequence models—where algorithmic choices show up directly in memory traffic, kernel design, and end-to-end latency. I like working at the boundary between architecture and software: profiling bottlenecks, forming clear hypotheses about where time/data is going, and turning that into measurable speedups.

        More broadly, I’m drawn to computer architecture (memory systems, interconnects, accelerators, HW/SW tradeoffs) and to the mathematical foundations that make good engineering decisions possible (probability/statistics, linear algebra, signal processing).

        I keep the theory grounded through hands-on accelerated computing work. For example, in my final semester at UBC I took CPEN 512 (Parallel and Configurable Computer Architecture), where I implemented dense linear algebra kernels (matmul, LU decomposition) across multiple parallel programming models (OpenMPI, pthreads, CUDA, Bluespec, Vectorblox). For the final project, I implemented a Cooley–Tukey FFT using CUDA and OpenMPI.
    design:
      columns: '1'
  - block: collection
    id: news
    content:
      title: Blog Posts
      subtitle: ''
      text: ''
      # Page type to display. E.g. post, talk, publication...
      page_type: post
      # Choose how many pages you would like to display (0 = all pages)
      count: 5
      # Filter on criteria
      filters:
        author: ""
        category: ""
        tag: ""
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ""
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc
    design:
      # Choose a layout view
      view: date-title-summary
      # Reduce spacing
      spacing:
        padding: [0, 0, 0, 0]
---

