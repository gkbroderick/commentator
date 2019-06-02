//---GULP DEPENDENCIES----
//Node.js libraries
var del = require('del');
var fs = require('fs');
var path = require('path');

// Gulp-only dependencies
var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
sass.compiler = require('node-sass');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var minimist = require('minimist');
var gulpif = require('gulp-if');
var autoprefixer = require('gulp-autoprefixer');
var cleanCSS = require('gulp-clean-css');

// Directory helper vars
var src = "frontend/gulp-src/";
var dist = "frontend/static/frontend";

var inputStyles = path.join(src, "scss/");
var outputStyles = path.join(dist, "styles/");

var inputScripts =  path.join(src, "js/");
var outputScripts = path.join(dist, "js/");


// ---- Minimist Output options ----- // for --arg passing to Node via command
// line
var knownOptions = {
  string : "out",
  default : {out : 'stage'}
}
var options = minimist(process.argv.slice(2), knownOptions);
console.log("Current Output Type: " + options.out);
console.log("Process non-stage production output with: gulp --out production");


gulp.task('styles', function() {
  // Stage Output
  if (options.out === "stage") {
    return gulp.src(path.join(inputStyles, 'compiler.scss'))
      .pipe(sourcemaps.init())
      .pipe(sass({outputStyle: 'expanded'}))
        .on('error', function(err) {
          console.error('Error', err.message);
        })
      .pipe(sourcemaps.write('sass_maps'))
      .pipe(gulp.dest(outputStyles))
  }
  // All other output
  else {
    return gulp.src(path.join(inputStyles, 'compiler.scss'))
      .pipe(sass())
      .on('error', function(err) {
        console.error('Error', err.message);
      })
      .pipe(autoprefixer({
        browsers: ['last 4 versions'],
        cascade: false
      }))
		  .pipe(cleanCSS())
      .pipe(gulp.dest(outputStyles))
  }
});

gulp.task('scripts', function() {
  return gulp.src([
     path.join(inputScripts, '/**/*.js'),
    ])

    ////if concatting
    // .pipe(concat('app.scripts.min.js')) // again, easier to just call it min

    .pipe(gulpif(options.out !== 'stage', uglify().on('error', gutil.log)))
    .pipe(gulp.dest(outputScripts));
});

gulp.task('copy-assets', function() {
  gulp.src(path.join(src, '**/*.+(jpg|jpeg|gif|png|svg|mp4|ogg|webm|eot|ttf|woff)'))
    .pipe(gulp.dest(path.join(dist,'')))
});


gulp.task('out', ['styles', 'scripts', 'copy-assets']);


// ** Watch Task Outputs **//
gulp.task('watch', ['styles', 'scripts', 'copy-assets'], function() {
    gulp.watch([inputStyles + '**/*.scss', inputStyles + '**/*.sass'], ['styles']);
    gulp.watch([inputScripts + '/js/**/*.js'], ['scripts']);
    gulp.watch([src + '**/*.+(jpg|jpeg|gif|png|svg|mp4|ogg|webm|ttf)'], ['copy-assets']);
});



// Default is stage-output watch
gulp.task('default', ['watch']);
