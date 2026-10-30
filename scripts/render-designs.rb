#!/usr/bin/env ruby
require 'jekyll'
require 'nokogiri'
require 'erb'
require 'json'
require 'fileutils'
require 'cgi'

Dir.chdir(File.expand_path('..', __dir__))
site = Jekyll::Site.new(Jekyll.configuration('quiet' => true))
site.read
FileUtils.mkdir_p('design-review/text')
site.posts.docs.each do |post|
  slug = post.basename_without_ext.sub(/^\d{4}-\d{1,2}-\d{1,2}-/, '')
  markdown = site.liquid_renderer.file(post.path).parse(post.content).render!(site.site_payload)
  header = "# #{post.data['title']}\n\nBy Mario Mendez · #{post.date.strftime('%Y-%m-%d')}\nOriginal: #{site.config['url']}#{post.url}\n\n"
  File.write("design-review/text/#{slug}.md", header + markdown)
end
posts = site.posts.docs.sort_by(&:date).reverse.map do |post|
  page = Nokogiri::HTML(File.read(File.join('_site', post.url.delete_prefix('/'))))
  body = page.at_css('#post section.text-left, #post.prose').inner_html
  { title: post.data['title'], date: post.date.strftime('%b %d, %Y'), iso: post.date.strftime('%Y-%m-%d'), year: post.date.year,
    slug: post.basename_without_ext.sub(/^\d{4}-\d{1,2}-\d{1,2}-/, ''), url: post.url,
    topics: post.data['category'] == 'startups' ? 'product teams' : post.data['category'] == 'Robotics' ? 'systems experiments' : 'experiments systems',
    body: body.gsub(/((?:href|src)=["'])\/(?!\/)/, '\1https://mariomendez.me/'),
    words: page.at_css('#post section.text-left, #post.prose').text.split.length }
end
summaries = {
  'road-to-seed-round' => 'From the Evotrux MVP to our seed round: finding a customer, running short on time, and deciding what to build.',
  'lessons-mvp-launch' => 'What I wish I’d known before launching Evotrux 2.0. Code standards, saying no, observability, and looking after the team.',
  'IROS' => 'We had to make two humanoid robots play a 15-minute set. Here’s how we did it.',
  'qualification-2019' => 'A record from the robotics competition years.',
  'fixmynotes' => 'An experiment in making handwritten notes easier to work with.',
  'fira-2018' => 'Lessons and experiences from a robotics competition in Taiwan.',
  'robocup' => 'Competing with the University of Manitoba Snobots at RoboCup.',
  'AUT' => 'AUTCup in Tehran with the University of Manitoba Snobots.'
}
posts.each { |p| p[:summary] = summaries.fetch(p[:slug], 'From the archive.') }
events = site.config['events'].map.with_index do |event, index|
  titles = ['Building Evotrux', 'Full-stack development at Evotrux', 'Software Developer · AGCO', 'B.Sc. Computer Science · University of Manitoba', 'Research & Technology Editor · The Manitoban', 'Software Developer Intern · 151 Research', 'IROS · Robot music', 'Innovation Lab · Wawanesa', 'Hack the North', 'FIRA · Taiwan', 'RoboCup', 'AUTCup · Tehran', 'A new chapter in Canada']
  {date: event['date'], description: event['description'], title: titles[index], image: '../../' + event['image'].delete_prefix('/')}
end
variants = [
  {id:'journal', number:'01', name:'The blog', subtitle:'Mario Mendez: software, products, teams.', tagline:'Hi, I’m Mario.', description:'I’m a CTO and founder. I like writing code, figuring out how systems work, and building things people find useful. This is where I write down what I learn.', rationale:'Dark background, off-white text, green links. Mono throughout; recent writing first.'},
  {id:'fieldguide', number:'02', name:'Notes by topic', subtitle:'Writing about systems, products, and teams.', tagline:'Writing', description:'Software, products, teams, and things I’ve tried. Some of these posts are lessons from building Evotrux. Others are from my time working with robots.', rationale:'A compact topic index with working filters. Green headings and a visible agent handoff.'},
  {id:'record', number:'03', name:'Work & writing', subtitle:'Mario Mendez: experience and writing.', tagline:'Work & writing', description:'I’m Mario, a CTO and founder. I’ve worked on freight software, IoT, and humanoid robots. Here’s some of that work, and what I’ve written about it.', rationale:'Mono navigation with Plex Sans for longer reading. Experience and related writing together.'}
]
personal_variants = [
  {slug:'cat', motif:'cat', name:'A cat in the margins', unchanged:true},
  {slug:'ride', motif:'ride', name:'The long route', unchanged:true},
  {slug:'summit', motif:'summit', name:'Still climbing', unchanged:false},
  {slug:'notebook', motif:'notebook', name:'Field notes', unchanged:false}
].map { |personal| variants.first.merge(personal) }
variants += personal_variants
motion_variants = [
  {slug:'scroll-bike', scroll:'bike', name:'A bike in the margin'},
  {slug:'scroll-summit', scroll:'summit', name:'The summit companion'},
  {slug:'scroll-trail', scroll:'trail', name:'A trail through the writing'}
].map { |motion| personal_variants.find { |personal| personal[:motif]=='summit' }.merge(motion) }
variants += motion_variants
pair_variants = [
  {slug:'pair-ridge', pair:'ridge', name:'The ascent / Switchbacks'},
  {slug:'pair-pass', pair:'pass', name:'High pass / The cyclist'},
  {slug:'pair-night', pair:'night', name:'After dark / The resting cat'},
  {slug:'pair-contour', pair:'contour', name:'Contour study / The runner'},
  {slug:'pair-traverse', pair:'traverse', name:'One more ridge / Elevation'},
  {slug:'pair-window', pair:'window', name:'The window seat / The wandering cat'}
].map { |pair| personal_variants.find { |personal| personal[:motif]=='summit' }.merge(pair) }
variants += pair_variants
quiet_variants = [
  {slug:'quiet-incline', pair:'quiet-incline', minimal:'incline', name:'A measured ascent'},
  {slug:'quiet-sisyphus', pair:'quiet-sisyphus', minimal:'sisyphus', name:'The quiet push'},
  {slug:'quiet-cairn', pair:'quiet-cairn', minimal:'cairn', name:'The cairn'}
].map { |quiet| pair_variants.find { |pair| pair[:pair]=='pass' }.merge(quiet) }
variants += quiet_variants
mountain_variants = [
  {slug:'mountain-ridge', pair:'mountain-ridge', mountain:'ridge', name:'Thin ridgeline'},
  {slug:'mountain-contour', pair:'mountain-contour', mountain:'contour', name:'Contour band'},
  {slug:'mountain-horizon', pair:'mountain-horizon', mountain:'horizon', name:'Layered horizon'}
].map { |mountain| quiet_variants.find { |quiet| quiet[:minimal]=='incline' }.merge(mountain) }
variants += mountain_variants
variants.each do |variant|
  directory = "design-review/#{variant[:slug] || variant[:id]}"
  FileUtils.mkdir_p(directory)
  pages = [{type:'home', file:'index.html'}, {type:'history',file:'history.html'}] + posts.map { |post| {type:'article',file:"#{post[:slug]}.html",post:post} }
  pages.each do |current|
    output = ERB.new(File.read(current[:type] == 'home' && variant[:motif] == 'notebook' ? 'design-review/templates/notebook.erb' : 'design-review/templates/page.erb'), trim_mode:'-').result(binding)
    File.write("#{directory}/#{current[:file]}", output)
  end
end
profile = {personal_interests:['Cats', 'Bicycles', 'Multi-day bike trips', 'Endurance running', 'Mountains as a metaphor for patient growth'], personal_experience:['Has run several marathons', 'Has taken multi-day bike trips'], name:'Mario Mendez', headline:'CTO and founder', description:'Building and learning about software systems, products, teams, communication, and technology.', source:'User briefs and existing repository, reviewed 2026-10-28', caveat:'Prototype data. Exact current title, title start date, and preferred biography need confirmation before production.', links:{website:site.config['url'],github:site.config['social'].find { |s| s['title']=='github' }['url']}, experience:events.map { |event| event.merge(image: site.config['url'] + event[:image].delete_prefix('../..')) }, writing:posts.map { |p| p.reject { |k,_| k==:body }.merge(url:site.config['url']+p[:url]) }}
File.write('design-review/profile.json',JSON.pretty_generate(profile)+"\n")
FileUtils.mkdir_p('design-review/agents')
File.write('design-review/agents/index.html', ERB.new(File.read('design-review/templates/agent.erb'), trim_mode:'-').result(binding))
profile_markdown = "# Mario Mendez\n\nCTO and founder. I like writing code, understanding systems, and building products people find useful.\n\nLocal design review, October 28, 2026. Proposed introduction from the user brief; professional history below comes from the existing site. Exact current title start date is not established.\n\n## Professional history\n\n"
events.each { |event| profile_markdown += "### #{event[:title]}\n\n#{event[:date]}\n\n#{event[:description]}\n\n" }
profile_markdown += "## Away from the keyboard\n\nFrom the user brief: Mario likes cats, bicycles, endurance sports, and mountains as a metaphor for slow growth. He has run several marathons and taken multi-day bike trips. No specific race results, routes, or mountaineering experience are established.\n\n## Public links\n\n- Website: #{site.config['url']}\n- GitHub: #{profile[:links][:github]}\n- LinkedIn: https://www.linkedin.com/in/mario-mendez-d/\n- Email: mmendezdiaz@outlook.com\n\n## Writing\n\nSee [the writing index](writing.md) for original sources and Markdown copies.\n"
File.write('design-review/profile.md', profile_markdown)
writing_markdown = "# Mario Mendez: writing\n\nLocal preview exports of existing articles. Summaries and topic assignments are proposed editorial additions. Original article body text is unchanged.\n\n"
posts.each { |post| writing_markdown += "## #{post[:title]}\n\nPublished #{post[:iso]}\n\n#{post[:summary]}\n\n- [Original article](#{site.config['url']}#{post[:url]})\n- [Markdown](text/#{post[:slug]}.md)\n\n" }
File.write('design-review/writing.md', writing_markdown.rstrip + "\n")
puts "Rendered #{variants.length} directions with #{posts.length} real articles and a history view each."
