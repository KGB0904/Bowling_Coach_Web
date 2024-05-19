class ScrollBar {
    constructor() {
        this.$scrollBar = document.getElementById('slider');
        this.video = document.getElementById('video');
        
        this.initSlider();
        this.addEventListeners();
    }

    initSlider() {
        noUiSlider.create(this.$scrollBar, {
            start: 0,
            range: {
                min: 0,
                max: 1 // This will be updated with the video's duration
            },
            step: 0.1,
            connect: [true, false],
            tooltips: true,
            format: {
                to: value => value.toFixed(2),
                from: value => parseFloat(value)
            }
        });
    }

    syncScrubberWithVideo() {
        this.$scrollBar.noUiSlider.updateOptions({
            range: {
                min: 0,
                max: this.video.duration
            }
        });
        this.$scrollBar.noUiSlider.set(this.video.currentTime);
    }

    syncVideoWithScrubber(values, handle) {
        this.video.currentTime = parseFloat(values[handle]);
    }

    addEventListeners() {
        this.video.addEventListener('loadedmetadata', () => this.syncScrubberWithVideo());

        this.video.addEventListener('timeupdate', () => {
            this.$scrollBar.noUiSlider.set(this.video.currentTime);
        });

        this.$scrollBar.noUiSlider.on('update', (values, handle) => {
            this.syncVideoWithScrubber(values, handle);
        });
    }
}

export default new ScrollBar();
