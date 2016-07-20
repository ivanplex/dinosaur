import javax.sound.sampled.AudioFormat;

/**
 * Created by ivan on 20/07/2016.
 */
public class AudioSetting {

    private float sampleRate;
    private int sampleSizeBits;
    private int channels;
    private boolean signed;
    private boolean bigEndian;

    public AudioSetting(){
        this.sampleRate = 16000.0F;
        this.sampleSizeBits = 16;
        this.channels = 1;
        this.signed = true;
        this.bigEndian = false;
    }


    public AudioFormat getAudioFormat() {
        return new AudioFormat(sampleRate, sampleSizeBits, channels, signed, bigEndian);
    }

    public void setSampleRate(float sampleRate) {
        this.sampleRate = sampleRate;
    }

    public void setSampleSizeBits(int sampleSizeBits) {
        this.sampleSizeBits = sampleSizeBits;
    }

    public void setChannels(int channels) {
        this.channels = channels;
    }

    public void setSigned(boolean signed) {
        this.signed = signed;
    }

    public void setBigEndian(boolean bigEndian) {
        this.bigEndian = bigEndian;
    }
}
