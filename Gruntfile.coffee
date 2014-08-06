module.exports = (grunt) ->
	grunt.initConfig
		pkg :
			grunt.file.readJSON 'package.json'

		
		#自动编译coffee文件
		coffee:
			build:
				expand:true
				cwd : 'app/static/dev/coffee'
				src : [ '**/*.coffee' ]
				dest : 'app/static/js'
				ext :'.js'

		#自动编译scss文件
		sass:
			dist:
				files: [{
						expand : true
						cwd : "app/static/dev/scss"
						src : ['**/*.scss']
						dest : 'app/static/css'
						ext : '.css'
					}]
		#查看文件变化				
		watch:
			options:
      			livereload: true
			scripts:
				files: [ '**/*.coffee','Gruntfile.coffee' ]
				tasks: ["coffee"]
				option: 
					spawn: false
			css:
				files :['**/*.scss']
				tasks : ["sass"]
				option:
					spawn :false
		#压缩js文件
		uglify:
			build:
				expand:true
				cwd: 'app/static/dev/js'
				src: '**/*.js'
				dest: 'app/static/js'
				ext : ".min.js"


	grunt.loadNpmTasks 'grunt-contrib-coffee'
	grunt.loadNpmTasks 'grunt-contrib-watch'
	grunt.loadNpmTasks('grunt-contrib-sass')
	grunt.loadNpmTasks "grunt-contrib-uglify"

	grunt.registerTask "default", ->
    	grunt.task.run [
    	  "coffee"
    	  "sass"
	      "watch"
    	]

    grunt.registerTask "build", ['coffee','sass',"watch"]
    grunt.registerTask "compress",["uglify"]
